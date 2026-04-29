// ─────────────────────────────────────────────────────────────────────────────
// Core data types shared across the synth engine and UI
// ─────────────────────────────────────────────────────────────────────────────

export type OscillatorType = 'sine' | 'square' | 'sawtooth' | 'triangle' | 'noise';

export interface AdsrParams {
  attack: number;   // seconds
  decay: number;    // seconds
  sustain: number;  // 0-1 amplitude
  release: number;  // seconds
}

export interface FilterParams {
  type: BiquadFilterType;
  frequency: number; // Hz
  Q: number;
  gain: number;      // dB (for peaking/shelf)
}

export interface OscillatorParams {
  type: OscillatorType;
  detune: number;    // cents
  volume: number;    // 0-1
}

export interface EffectsParams {
  delayTime: number;     // seconds
  delayFeedback: number; // 0-1
  delayWet: number;      // 0-1

  reverbDecay: number;   // seconds (simulated via convolver)
  reverbWet: number;     // 0-1

  distortionAmount: number; // 0-1
  distortionWet: number;    // 0-1
}

export interface InstrumentParams {
  name: string;
  oscillators: OscillatorParams[];
  adsr: AdsrParams;
  filter: FilterParams;
  effects: EffectsParams;
  volume: number; // 0-1 channel volume
  pan: number;    // -1 to 1
}

export interface Step {
  active: boolean;
  note: number;   // MIDI note number (0-127)
  velocity: number; // 0-1
}

export interface Pattern {
  id: string;
  name: string;
  steps: Step[][];      // [trackIndex][stepIndex]
  stepCount: number;    // 8, 16, 32
  instruments: InstrumentParams[];
}

export interface Song {
  name: string;
  bpm: number;
  swing: number;        // 0-1 (0 = straight, 1 = max swing)
  patterns: Pattern[];
  sequence: string[];   // ordered list of pattern IDs
  masterVolume: number; // 0-1
}

export const DEFAULT_ADSR: AdsrParams = {
  attack: 0.005,
  decay: 0.1,
  sustain: 0.7,
  release: 0.2,
};

export const DEFAULT_FILTER: FilterParams = {
  type: 'lowpass',
  frequency: 8000,
  Q: 1,
  gain: 0,
};

export const DEFAULT_EFFECTS: EffectsParams = {
  delayTime: 0.375,
  delayFeedback: 0.3,
  delayWet: 0,
  reverbDecay: 2.0,
  reverbWet: 0,
  distortionAmount: 0.5,
  distortionWet: 0,
};

export const DEFAULT_OSCILLATOR: OscillatorParams = {
  type: 'sawtooth',
  detune: 0,
  volume: 1,
};

export const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

export function midiToFrequency(midi: number): number {
  return 440 * Math.pow(2, (midi - 69) / 12);
}

export function midiToName(midi: number): string {
  const octave = Math.floor(midi / 12) - 1;
  return `${NOTE_NAMES[midi % 12]}${octave}`;
}
