// ─────────────────────────────────────────────────────────────────────────────
// Step Sequencer Engine
//
// Uses the Web Audio API clock (AudioContext.currentTime) for sample-accurate
// scheduling. A lookahead scheduler fires every SCHEDULE_INTERVAL ms and
// queues notes up to LOOKAHEAD seconds ahead, preventing audio dropouts.
//
// Swing is implemented by delaying every even-numbered step by a fraction of
// a 16th note.
// ─────────────────────────────────────────────────────────────────────────────

import type { Song, Pattern, Step } from './types';
import { InstrumentChannel } from './synth';

const LOOKAHEAD = 0.1;        // seconds to schedule ahead
const SCHEDULE_INTERVAL = 25; // ms between scheduler ticks

export type SequencerEventType = 'step' | 'patternChange' | 'stop';

export interface SequencerEvent {
  type: SequencerEventType;
  step?: number;
  patternIndex?: number;
}

export type SequencerListener = (e: SequencerEvent) => void;

export class Sequencer {
  private ctx: AudioContext;
  private masterBus: GainNode;
  private channels: InstrumentChannel[] = [];
  private song: Song | null = null;
  private pattern: Pattern | null = null;

  private isPlaying = false;
  private currentStep = 0;
  private currentPatternSeqIdx = 0;  // index into song.sequence[]
  private nextNoteTime = 0;
  private timerId: ReturnType<typeof setInterval> | null = null;
  private listeners: SequencerListener[] = [];

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
    this.masterBus = ctx.createGain();
    this.masterBus.connect(ctx.destination);
  }

  get audioContext(): AudioContext { return this.ctx; }
  get master(): GainNode { return this.masterBus; }

  // ── Song / pattern loading ────────────────────────────────────────────────

  loadSong(song: Song): void {
    this.stop();
    this.song = song;
    this.masterBus.gain.value = song.masterVolume;
    if (song.patterns.length > 0) {
      this.loadPattern(song.patterns[0]);
    }
  }

  loadPattern(pattern: Pattern): void {
    this.pattern = pattern;
    this.rebuildChannels();
  }

  private rebuildChannels(): void {
    for (const ch of this.channels) ch.allNotesOff();
    this.channels = [];
    if (!this.pattern) return;
    for (const inst of this.pattern.instruments) {
      this.channels.push(new InstrumentChannel(this.ctx, inst, this.masterBus));
    }
  }

  updateInstrument(trackIdx: number, params: Pattern['instruments'][0]): void {
    if (this.channels[trackIdx]) {
      this.channels[trackIdx].updateParams(params);
    }
    if (this.pattern) {
      this.pattern.instruments[trackIdx] = params;
    }
  }

  // ── Transport ─────────────────────────────────────────────────────────────

  play(): void {
    if (this.isPlaying) return;
    if (this.ctx.state === 'suspended') this.ctx.resume();
    this.isPlaying = true;
    this.currentStep = 0;
    this.currentPatternSeqIdx = 0;
    this.nextNoteTime = this.ctx.currentTime + 0.05;

    // Load first pattern in sequence if song is set
    if (this.song && this.song.sequence.length > 0) {
      const pid = this.song.sequence[0]!;
      const pat = this.song.patterns.find(p => p.id === pid);
      if (pat) this.loadPattern(pat);
    }

    this.timerId = setInterval(() => this.schedule(), SCHEDULE_INTERVAL);
  }

  stop(): void {
    if (!this.isPlaying) return;
    this.isPlaying = false;
    if (this.timerId !== null) {
      clearInterval(this.timerId);
      this.timerId = null;
    }
    for (const ch of this.channels) ch.allNotesOff();
    this.emit({ type: 'stop' });
  }

  toggle(): void {
    this.isPlaying ? this.stop() : this.play();
  }

  get playing(): boolean { return this.isPlaying; }
  get step(): number { return this.currentStep; }

  // ── Scheduler ─────────────────────────────────────────────────────────────

  private schedule(): void {
    while (this.nextNoteTime < this.ctx.currentTime + LOOKAHEAD) {
      this.scheduleStep(this.currentStep, this.nextNoteTime);
      this.advanceStep();
    }
  }

  private scheduleStep(step: number, time: number): void {
    if (!this.pattern) return;
    const stepTime = time;
    for (let t = 0; t < this.pattern.instruments.length; t++) {
      const s: Step = this.pattern.steps[t]?.[step];
      if (s?.active && this.channels[t]) {
        this.channels[t].noteOn(s.note, s.velocity, stepTime);
        // Schedule note-off after half a step (staccato feel; ADSR handles actual release)
        const halfStep = this.stepDuration() * 0.45;
        this.scheduleNoteOff(t, s.note, stepTime + halfStep);
      }
    }
    // Notify UI at approximately the right time
    const delay = (time - this.ctx.currentTime) * 1000;
    setTimeout(() => this.emit({ type: 'step', step }), Math.max(0, delay));
  }

  private scheduleNoteOff(trackIdx: number, note: number, time: number): void {
    const delay = Math.max(0, (time - this.ctx.currentTime) * 1000);
    setTimeout(() => {
      if (this.channels[trackIdx]) this.channels[trackIdx].noteOff(note);
    }, delay);
  }

  private advanceStep(): void {
    if (!this.pattern) return;
    const swing = this.song?.swing ?? 0;
    const baseDur = this.stepDuration();
    // Swing: odd steps are delayed relative to even
    const swingOffset = (this.currentStep % 2 === 1) ? baseDur * swing * 0.33 : 0;
    this.nextNoteTime += baseDur + swingOffset;
    this.currentStep = (this.currentStep + 1) % this.pattern.stepCount;

    // Pattern sequencing: advance to next pattern when step wraps
    if (this.currentStep === 0 && this.song && this.song.sequence.length > 1) {
      this.currentPatternSeqIdx =
        (this.currentPatternSeqIdx + 1) % this.song.sequence.length;
      const pid = this.song.sequence[this.currentPatternSeqIdx];
      const pat = this.song.patterns.find(p => p.id === pid);
      if (pat) {
        this.loadPattern(pat);
        this.emit({ type: 'patternChange', patternIndex: this.currentPatternSeqIdx });
      }
    }
  }

  private stepDuration(): number {
    const bpm = this.song?.bpm ?? 120;
    // One 16th note = one step at standard resolution
    return 60 / bpm / 4;
  }

  // ── Event bus ─────────────────────────────────────────────────────────────

  on(listener: SequencerListener): () => void {
    this.listeners.push(listener);
    return () => { this.listeners = this.listeners.filter(l => l !== listener); };
  }

  private emit(e: SequencerEvent): void {
    for (const l of this.listeners) l(e);
  }

  // ── Preview (play a single note immediately) ──────────────────────────────

  previewNote(trackIdx: number, midi: number, durationSec = 0.3): void {
    if (!this.channels[trackIdx]) return;
    if (this.ctx.state === 'suspended') this.ctx.resume();
    const t = this.ctx.currentTime;
    this.channels[trackIdx].noteOn(midi, 0.8, t);
    setTimeout(() => this.channels[trackIdx].noteOff(midi), durationSec * 1000);
  }

  // ── Offline WAV rendering ─────────────────────────────────────────────────

  async renderToBuffer(song: Song): Promise<AudioBuffer> {
    const totalSteps = song.sequence.reduce((acc, pid) => {
      const p = song.patterns.find(x => x.id === pid);
      return acc + (p?.stepCount ?? 16);
    }, 0);

    const stepDur = 60 / song.bpm / 4;
    const totalDuration = totalSteps * stepDur + 2; // 2s tail for effects
    const sampleRate = this.ctx.sampleRate;

    const offCtx = new OfflineAudioContext(2, Math.ceil(totalDuration * sampleRate), sampleRate);
    const masterBus = offCtx.createGain();
    masterBus.gain.value = song.masterVolume;
    masterBus.connect(offCtx.destination);

    let time = 0.05;

    for (const pid of song.sequence) {
      const pattern = song.patterns.find(p => p.id === pid);
      if (!pattern) continue;

      const offChannels = pattern.instruments.map(
        inst => new InstrumentChannel(offCtx as unknown as AudioContext, inst, masterBus as unknown as GainNode),
      );

      for (let step = 0; step < pattern.stepCount; step++) {
        for (let t = 0; t < pattern.instruments.length; t++) {
          const s = pattern.steps[t]?.[step];
          if (s?.active && offChannels[t]) {
            offChannels[t].noteOn(s.note, s.velocity, time);
          }
        }
        time += stepDur;
      }
    }

    return offCtx.startRendering();
  }
}
