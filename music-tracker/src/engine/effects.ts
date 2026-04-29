// ─────────────────────────────────────────────────────────────────────────────
// Effects chain: Delay → Reverb → Distortion
// Each effect is a parallel wet/dry blend wired into the channel insert.
// ─────────────────────────────────────────────────────────────────────────────

import type { EffectsParams } from './types';

export class DelayEffect {
  private dry: GainNode;
  private wet: GainNode;
  private delay: DelayNode;
  private feedback: GainNode;
  readonly input: GainNode;
  readonly output: GainNode;

  constructor(ctx: AudioContext) {
    this.input = ctx.createGain();
    this.output = ctx.createGain();
    this.dry = ctx.createGain();
    this.wet = ctx.createGain();
    this.delay = ctx.createDelay(2.0);
    this.feedback = ctx.createGain();

    // Dry path
    this.input.connect(this.dry);
    this.dry.connect(this.output);

    // Wet path: input → delay → wet out; feedback loop
    this.input.connect(this.delay);
    this.delay.connect(this.feedback);
    this.feedback.connect(this.delay);
    this.delay.connect(this.wet);
    this.wet.connect(this.output);
  }

  update(p: EffectsParams): void {
    const ctx = this.input.context;
    const t = ctx.currentTime;
    this.delay.delayTime.setTargetAtTime(p.delayTime, t, 0.01);
    this.feedback.gain.setTargetAtTime(Math.min(p.delayFeedback, 0.95), t, 0.01);
    this.wet.gain.setTargetAtTime(p.delayWet, t, 0.01);
    this.dry.gain.setTargetAtTime(1 - p.delayWet * 0.5, t, 0.01);
  }
}

/** Impulse-response based reverb using a generated IR buffer */
export class ReverbEffect {
  private dry: GainNode;
  private wet: GainNode;
  private convolver: ConvolverNode;
  readonly input: GainNode;
  readonly output: GainNode;
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
    this.input = ctx.createGain();
    this.output = ctx.createGain();
    this.dry = ctx.createGain();
    this.wet = ctx.createGain();
    this.convolver = ctx.createConvolver();

    this.input.connect(this.dry);
    this.dry.connect(this.output);

    this.input.connect(this.convolver);
    this.convolver.connect(this.wet);
    this.wet.connect(this.output);

    this.buildIR(2.0);
  }

  /** Generate a simple exponentially-decaying noise IR */
  buildIR(decaySeconds: number): void {
    const rate = this.ctx.sampleRate;
    const length = Math.ceil(rate * decaySeconds);
    const buffer = this.ctx.createBuffer(2, length, rate);
    for (let ch = 0; ch < 2; ch++) {
      const data = buffer.getChannelData(ch);
      for (let i = 0; i < length; i++) {
        // Exponential decay with noise, slight early-reflection peak at ~20ms
        const decay = Math.pow(1 - i / length, 3);
        const earlyBoost = i < rate * 0.02 ? 1.5 : 1.0;
        data[i] = (Math.random() * 2 - 1) * decay * earlyBoost;
      }
    }
    this.convolver.buffer = buffer;
  }

  update(p: EffectsParams): void {
    const ctx = this.ctx;
    const t = ctx.currentTime;
    this.wet.gain.setTargetAtTime(p.reverbWet * 0.5, t, 0.01);
    this.dry.gain.setTargetAtTime(1 - p.reverbWet * 0.3, t, 0.01);
    this.buildIR(Math.max(0.1, p.reverbDecay));
  }
}

/** Waveshaper distortion with soft/hard clipping */
export class DistortionEffect {
  private dry: GainNode;
  private wet: GainNode;
  private shaper: WaveShaperNode;
  private preGain: GainNode;
  readonly input: GainNode;
  readonly output: GainNode;

  constructor(ctx: AudioContext) {
    this.input = ctx.createGain();
    this.output = ctx.createGain();
    this.dry = ctx.createGain();
    this.wet = ctx.createGain();
    this.shaper = ctx.createWaveShaper();
    this.preGain = ctx.createGain();

    this.shaper.oversample = '4x';

    this.input.connect(this.dry);
    this.dry.connect(this.output);

    this.input.connect(this.preGain);
    this.preGain.connect(this.shaper);
    this.shaper.connect(this.wet);
    this.wet.connect(this.output);

    this.buildCurve(0.5);
  }

  /** Soft-clip using tanh approximation, k controls hardness */
  buildCurve(amount: number): void {
    const samples = 256;
    const curve = new Float32Array(samples);
    const k = amount * 200;
    for (let i = 0; i < samples; i++) {
      const x = (i * 2) / samples - 1;
      curve[i] = k === 0 ? x : ((1 + k / 100) * x) / (1 + (k / 100) * Math.abs(x));
    }
    this.shaper.curve = curve;
  }

  update(p: EffectsParams): void {
    const ctx = this.input.context;
    const t = ctx.currentTime;
    this.buildCurve(p.distortionAmount);
    this.preGain.gain.setTargetAtTime(1 + p.distortionAmount * 4, t, 0.01);
    this.wet.gain.setTargetAtTime(p.distortionWet * 0.7, t, 0.01);
    this.dry.gain.setTargetAtTime(1 - p.distortionWet * 0.5, t, 0.01);
  }
}
