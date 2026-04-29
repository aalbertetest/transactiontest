// ─────────────────────────────────────────────────────────────────────────────
// Synth Voice and Channel
//
// Architecture per channel:
//   [OSC1 + OSC2 + OSC3] → gain mixer
//     → filter (BiquadFilterNode)
//     → ADSR envelope (GainNode)
//     → DistortionEffect
//     → DelayEffect
//     → ReverbEffect
//     → pan (StereoPannerNode)
//     → channel volume (GainNode)
//     → master bus
//
// Each note triggers a new Voice (one-shot node set). Voices are pooled and
// auto-released after release phase completes to avoid node accumulation.
// ─────────────────────────────────────────────────────────────────────────────

import type { InstrumentParams, AdsrParams, OscillatorParams } from './types';
import { midiToFrequency } from './types';
import { DelayEffect, ReverbEffect, DistortionEffect } from './effects';

// ── Noise source helper ────────────────────────────────────────────────────

function createNoiseSource(ctx: AudioContext): AudioBufferSourceNode {
  const bufSize = ctx.sampleRate * 2;
  const buf = ctx.createBuffer(1, bufSize, ctx.sampleRate);
  const data = buf.getChannelData(0);
  for (let i = 0; i < bufSize; i++) data[i] = Math.random() * 2 - 1;
  const src = ctx.createBufferSource();
  src.buffer = buf;
  src.loop = true;
  return src;
}

// ── Single triggered voice ─────────────────────────────────────────────────

class Voice {
  private sources: (OscillatorNode | AudioBufferSourceNode)[] = [];
  private oscGain: GainNode;
  private filter: BiquadFilterNode;
  private envelope: GainNode;
  private ctx: AudioContext;

  constructor(
    ctx: AudioContext,
    midi: number,
    velocity: number,
    params: InstrumentParams,
    destination: AudioNode,
    startTime: number,
  ) {
    this.ctx = ctx;
    this.oscGain = ctx.createGain();
    this.filter = ctx.createBiquadFilter();
    this.envelope = ctx.createGain();

    // Build oscillator stack
    for (const osc of params.oscillators) {
      this.addOscillator(osc, midi);
    }

    // Filter
    this.filter.type = params.filter.type;
    this.filter.frequency.value = params.filter.frequency;
    this.filter.Q.value = params.filter.Q;
    this.filter.gain.value = params.filter.gain;

    // Connect: oscs → filter → envelope → destination
    this.oscGain.connect(this.filter);
    this.filter.connect(this.envelope);
    this.envelope.connect(destination);

    // Apply ADSR
    this.applyAdsr(params.adsr, velocity, startTime);

    // Start all sources
    for (const src of this.sources) src.start(startTime);
  }

  private addOscillator(p: OscillatorParams, midi: number): void {
    const ctx = this.ctx;
    const freq = midiToFrequency(midi);
    const volGain = ctx.createGain();
    volGain.gain.value = p.volume;

    if (p.type === 'noise') {
      const src = createNoiseSource(ctx);
      src.connect(volGain);
      this.sources.push(src);
    } else {
      const osc = ctx.createOscillator();
      osc.type = p.type;
      osc.frequency.value = freq;
      osc.detune.value = p.detune;
      osc.connect(volGain);
      this.sources.push(osc);
    }

    volGain.connect(this.oscGain);
  }

  private applyAdsr(adsr: AdsrParams, velocity: number, t: number): void {
    const gain = this.envelope.gain;
    const peak = velocity * 0.9;
    gain.setValueAtTime(0, t);
    gain.linearRampToValueAtTime(peak, t + adsr.attack);
    gain.linearRampToValueAtTime(peak * adsr.sustain, t + adsr.attack + adsr.decay);
  }

  release(adsr: AdsrParams, releaseTime: number): number {
    const gain = this.envelope.gain;
    const t = this.ctx.currentTime;
    gain.cancelScheduledValues(t);
    gain.setValueAtTime(gain.value, t);
    gain.linearRampToValueAtTime(0, t + adsr.release);

    const stopTime = t + adsr.release + 0.05;
    for (const src of this.sources) {
      try { src.stop(stopTime); } catch { /* already stopped */ }
    }
    return releaseTime + adsr.release + 0.1;
  }

  stop(): void {
    const t = this.ctx.currentTime;
    for (const src of this.sources) {
      try { src.stop(t); } catch { /* already stopped */ }
    }
    this.envelope.gain.setValueAtTime(0, t);
  }
}

// ── Instrument channel (persists for lifetime of pattern playback) ─────────

export class InstrumentChannel {
  readonly distortion: DistortionEffect;
  readonly delay: DelayEffect;
  readonly reverb: ReverbEffect;
  private pan: StereoPannerNode;
  private volume: GainNode;
  private activeVoices: Map<number, Voice> = new Map();
  readonly insertPoint: GainNode; // voices connect here
  private ctx: AudioContext;
  private params: InstrumentParams;

  constructor(ctx: AudioContext, params: InstrumentParams, masterBus: GainNode) {
    this.ctx = ctx;
    this.params = params;

    this.insertPoint = ctx.createGain();
    this.distortion = new DistortionEffect(ctx);
    this.delay = new DelayEffect(ctx);
    this.reverb = new ReverbEffect(ctx);
    this.pan = ctx.createStereoPanner();
    this.volume = ctx.createGain();

    // Chain: insert → distortion → delay → reverb → pan → volume → master
    this.insertPoint.connect(this.distortion.input);
    this.distortion.output.connect(this.delay.input);
    this.delay.output.connect(this.reverb.input);
    this.reverb.output.connect(this.pan);
    this.pan.connect(this.volume);
    this.volume.connect(masterBus);

    this.updateParams(params);
  }

  updateParams(p: InstrumentParams): void {
    this.params = p;
    const t = this.ctx.currentTime;
    this.pan.pan.setTargetAtTime(p.pan, t, 0.01);
    this.volume.gain.setTargetAtTime(p.volume, t, 0.01);
    this.distortion.update(p.effects);
    this.delay.update(p.effects);
    this.reverb.update(p.effects);
  }

  noteOn(midi: number, velocity: number, startTime: number): void {
    // Retrigger: stop old voice on same note
    if (this.activeVoices.has(midi)) {
      this.activeVoices.get(midi)!.stop();
    }
    const voice = new Voice(
      this.ctx, midi, velocity, this.params,
      this.insertPoint, startTime,
    );
    this.activeVoices.set(midi, voice);
  }

  noteOff(midi: number): void {
    const voice = this.activeVoices.get(midi);
    if (voice) {
      voice.release(this.params.adsr, this.ctx.currentTime);
      this.activeVoices.delete(midi);
    }
  }

  allNotesOff(): void {
    for (const [, voice] of this.activeVoices) voice.stop();
    this.activeVoices.clear();
  }
}
