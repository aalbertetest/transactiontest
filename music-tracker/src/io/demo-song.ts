// ─────────────────────────────────────────────────────────────────────────────
// Demo song: "Neon Pulse" – a four-on-the-floor techno demo with four tracks:
//   0: Kick drum  (noise burst + sine thump)
//   1: Hi-hat     (noise, short decay)
//   2: Bass       (sawtooth, filter sweep)
//   3: Lead       (square wave, delay + reverb)
//
// Pattern A: main groove (16 steps)
// Pattern B: break (16 steps, sparser hi-hat, lead variation)
// ─────────────────────────────────────────────────────────────────────────────

import type { Song, Pattern, InstrumentParams, Step } from '../engine/types';
import { DEFAULT_EFFECTS } from '../engine/types';

function emptySteps(tracks: number, steps: number): Step[][] {
  return Array.from({ length: tracks }, () =>
    Array.from({ length: steps }, () => ({ active: false, note: 60, velocity: 0.8 }))
  );
}

// ── Instruments ───────────────────────────────────────────────────────────

const kickInst: InstrumentParams = {
  name: 'Kick',
  oscillators: [
    { type: 'sine', detune: 0, volume: 1.0 },
    { type: 'noise', detune: 0, volume: 0.15 },
  ],
  adsr: { attack: 0.002, decay: 0.25, sustain: 0, release: 0.1 },
  filter: { type: 'lowpass', frequency: 200, Q: 1, gain: 0 },
  effects: { ...DEFAULT_EFFECTS },
  volume: 0.9,
  pan: 0,
};

const hihatInst: InstrumentParams = {
  name: 'Hi-hat',
  oscillators: [
    { type: 'noise', detune: 0, volume: 1.0 },
  ],
  adsr: { attack: 0.001, decay: 0.06, sustain: 0, release: 0.04 },
  filter: { type: 'highpass', frequency: 8000, Q: 1.5, gain: 0 },
  effects: { ...DEFAULT_EFFECTS },
  volume: 0.45,
  pan: 0.2,
};

const bassInst: InstrumentParams = {
  name: 'Bass',
  oscillators: [
    { type: 'sawtooth', detune: 0, volume: 0.8 },
    { type: 'sawtooth', detune: -7, volume: 0.3 },
  ],
  adsr: { attack: 0.005, decay: 0.1, sustain: 0.6, release: 0.08 },
  filter: { type: 'lowpass', frequency: 700, Q: 6, gain: 0 },
  effects: { ...DEFAULT_EFFECTS, distortionAmount: 0.3, distortionWet: 0.25 },
  volume: 0.75,
  pan: -0.1,
};

const leadInst: InstrumentParams = {
  name: 'Lead',
  oscillators: [
    { type: 'square', detune: 0, volume: 0.6 },
    { type: 'sawtooth', detune: 1200, volume: 0.35 }, // +1 octave
  ],
  adsr: { attack: 0.01, decay: 0.15, sustain: 0.5, release: 0.3 },
  filter: { type: 'lowpass', frequency: 3000, Q: 3, gain: 0 },
  effects: {
    ...DEFAULT_EFFECTS,
    delayTime: 0.375,
    delayFeedback: 0.35,
    delayWet: 0.35,
    reverbDecay: 1.8,
    reverbWet: 0.25,
  },
  volume: 0.55,
  pan: 0.15,
};

// ── Pattern A: Main groove ────────────────────────────────────────────────

function buildPatternA(): Pattern {
  const steps = emptySteps(4, 16);

  // Kick: 4-on-the-floor
  [0, 4, 8, 12].forEach(i => { steps[0][i] = { active: true, note: 36, velocity: 1.0 }; });

  // Hi-hat: 8th notes with accent on 1 and 9
  [0, 2, 4, 6, 8, 10, 12, 14].forEach(i => {
    steps[1][i] = { active: true, note: 42, velocity: i % 8 === 0 ? 0.85 : 0.55 };
  });

  // Bass: syncopated pattern – MIDI 36=C2, 38=D2, 43=G2, 31=G1
  const bassLine: [number, number, number][] = [
    [0, 36, 1.0], [1, 36, 0.6], [3, 43, 0.8],
    [4, 36, 1.0], [6, 38, 0.7], [7, 31, 0.65],
    [8, 36, 1.0], [9, 36, 0.6], [11, 43, 0.8],
    [12, 36, 1.0], [14, 38, 0.7], [15, 31, 0.65],
  ];
  bassLine.forEach(([i, note, vel]) => {
    steps[2][i] = { active: true, note, velocity: vel };
  });

  // Lead melody – MIDI: C4=60, E4=64, G4=67, A4=69, Bb4=70
  const leadLine: [number, number, number][] = [
    [0, 60, 0.8], [2, 64, 0.7], [4, 67, 0.75],
    [6, 69, 0.65], [8, 70, 0.8], [10, 69, 0.6],
    [12, 67, 0.75], [14, 64, 0.7],
  ];
  leadLine.forEach(([i, note, vel]) => {
    steps[3][i] = { active: true, note, velocity: vel };
  });

  return {
    id: 'pattern-a',
    name: 'Main Groove',
    steps,
    stepCount: 16,
    instruments: [kickInst, hihatInst, bassInst, leadInst],
  };
}

// ── Pattern B: Break ──────────────────────────────────────────────────────

function buildPatternB(): Pattern {
  const steps = emptySteps(4, 16);

  // Kick: only on 1 and 9
  [0, 8].forEach(i => { steps[0][i] = { active: true, note: 36, velocity: 1.0 }; });

  // Hi-hat: quarter notes only
  [0, 4, 8, 12].forEach(i => {
    steps[1][i] = { active: true, note: 42, velocity: 0.6 };
  });

  // Bass: sparse
  [[0, 36, 1.0], [5, 43, 0.75], [8, 36, 1.0], [13, 38, 0.7]].forEach(([i, note, vel]) => {
    steps[2][i] = { active: true, note: note as number, velocity: vel as number };
  });

  // Lead: climbing phrase
  const breakLead: [number, number, number][] = [
    [0, 60, 0.7], [1, 62, 0.6], [2, 64, 0.65], [3, 65, 0.6],
    [4, 67, 0.75], [6, 69, 0.7], [8, 70, 0.8],
    [10, 72, 0.75], [12, 70, 0.7], [14, 67, 0.65],
  ];
  breakLead.forEach(([i, note, vel]) => {
    steps[3][i] = { active: true, note, velocity: vel };
  });

  return {
    id: 'pattern-b',
    name: 'Break',
    steps,
    stepCount: 16,
    instruments: [kickInst, hihatInst, bassInst, leadInst],
  };
}

// ── Song ──────────────────────────────────────────────────────────────────

export const DEMO_SONG: Song = {
  name: 'Neon Pulse',
  bpm: 128,
  swing: 0,
  patterns: [buildPatternA(), buildPatternB()],
  sequence: ['pattern-a', 'pattern-a', 'pattern-b', 'pattern-a'],
  masterVolume: 0.85,
};
