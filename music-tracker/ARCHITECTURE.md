# Music Tracker – Synth Architecture

## Overview

The tracker is a browser-only application built with **TypeScript** and the **Web Audio API**. There is no server, no external audio library, and no WASM — just the native WebAudio graph exposed through standard DOM APIs.

```
src/
├── engine/
│   ├── types.ts        Core data types (Song, Pattern, Step, InstrumentParams …)
│   ├── synth.ts        Voice & InstrumentChannel – per-note audio node graph
│   ├── effects.ts      DelayEffect, ReverbEffect, DistortionEffect
│   └── sequencer.ts    Step sequencer, lookahead scheduler, WAV offline renderer
├── io/
│   ├── demo-song.ts    Pre-built demo composition "Neon Pulse"
│   ├── json.ts         Save / load songs as JSON files or localStorage
│   └── wav.ts          16-bit PCM WAV encoder + browser download
└── ui/
    ├── App.ts                  Root application controller
    ├── StepGrid.ts             Step matrix UI (toggle, highlight, note popup)
    ├── InstrumentEditorPanel.ts  Tabbed wrapper around InstrumentEditor
    ├── InstrumentEditor.ts     Per-track knob/slider controls
    └── PatternManager.ts       Pattern list & arrangement sequencer
```

---

## Audio Signal Chain

Each **InstrumentChannel** creates a fixed subgraph that lives for the lifetime of the loaded pattern:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  InstrumentChannel                                                            │
│                                                                              │
│  ┌────────┐ ┌────────┐ ┌────────┐                                            │
│  │ OSC 1  │ │ OSC 2  │ │ OSC 3  │  (up to 3 per track, layered)              │
│  └───┬────┘ └───┬────┘ └───┬────┘                                            │
│      │ GainNode │  GainNode │  GainNode  (per-osc volume)                    │
│      └──────────┴──────────┘                                                 │
│                 │ GainNode (insertPoint)                                      │
│                 │                                                             │
│         ┌───────▼────────┐                                                   │
│         │ BiquadFilter   │  (type, freq, Q, gain)                            │
│         └───────┬────────┘                                                   │
│                 │                                                             │
│         ┌───────▼────────┐                                                   │
│         │ ADSR envelope  │  (GainNode driven by linearRamp)                  │
│         └───────┬────────┘                                                   │
│                 │                                                             │
│  ┌──────────────▼──────────────────────────────────────────────────────┐     │
│  │  DistortionEffect                                                    │     │
│  │   input ──┬── dry GainNode ──────────────────────────────┐          │     │
│  │           └── preGain → WaveShaperNode (4× oversample)   │          │     │
│  │                         └── wet GainNode ─────────────────┤          │     │
│  │                                                           output     │     │
│  └──────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐     │
│  │  DelayEffect                                                          │     │
│  │   input ──┬── dry GainNode ──────────────────────────────┐           │     │
│  │           └── DelayNode (0–2 s) ──┐                       │           │     │
│  │                    ↑              │                        │           │     │
│  │               feedback GainNode ←─┘                       │           │     │
│  │                                  └── wet GainNode ─────────┤           │     │
│  │                                                            output      │     │
│  └───────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐     │
│  │  ReverbEffect                                                         │     │
│  │   input ──┬── dry GainNode ──────────────────────────────┐           │     │
│  │           └── ConvolverNode (generated IR buffer) ────────┤           │     │
│  │                                                wet GainNode           │     │
│  │                                                            output      │     │
│  └───────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│         ┌───────▼────────┐                                                   │
│         │ StereoPanner   │  (pan: -1 … +1)                                   │
│         └───────┬────────┘                                                   │
│                 │                                                             │
│         ┌───────▼────────┐                                                   │
│         │ channel GainNode│  (volume: 0 … 1)                                  │
│         └───────┬────────┘                                                   │
└─────────────────┼────────────────────────────────────────────────────────────┘
                  │
          master GainNode (masterVolume)
                  │
          AudioContext.destination
```

---

## Oscillators

Each instrument can stack up to **three oscillators**. Each supports:

| Type       | Description                                             |
|------------|---------------------------------------------------------|
| `sine`     | Pure tone, fundamental only                             |
| `square`   | Odd harmonics, bright and reedy                         |
| `sawtooth` | All harmonics, rich and buzzy                           |
| `triangle` | Odd harmonics, softer than square                       |
| `noise`    | White noise (looped pre-generated buffer, 2 s)          |

Parameters per oscillator:
- **Detune** (cents, ±1200) – shifts pitch independent of note; useful for unison chorusing
- **Volume** (0–1) – mix level within the oscillator stack

---

## ADSR Envelope

The envelope modulates a `GainNode` that sits after the filter:

```
amplitude
   peak│  ·
       │ · ·
sustain│·    ·········
       │              ·
     0 ├──────────────────► time
       │  A   D   S     R
```

- **Attack** – linear ramp from 0 → peak (velocity-scaled)
- **Decay** – linear ramp from peak → sustain level
- **Sustain** – held amplitude (0–1, relative to peak)
- **Release** – exponential ramp to 0, triggered on note-off

Each note creates a new **Voice** (a short-lived OscillatorNode/BufferSourceNode set). Voices automatically stop after the release phase, freeing resources.

---

## Filter

A single `BiquadFilterNode` per voice positioned between the oscillator mixer and the envelope. Supported modes from the Web Audio API:

- `lowpass` / `highpass` / `bandpass` / `notch` / `allpass` / `peaking`

Parameters:
- **Frequency** (20 Hz – 20 kHz)
- **Q** (resonance, 0.001–30)
- **Gain** (dB, for peaking/shelf modes)

---

## Effects

All three effects use a **parallel wet/dry blend** so dry signal is always preserved.

### Delay

```
input ──► dry ───────────────► output
     └──► DelayNode ──► feedback loop ──► wet ──► output
```
- Delay time: 0–2 s (fractional beat values like 0.375 s = 3/8 at 120 BPM)
- Feedback: capped at 0.95 to prevent runaway
- Wet: 0–1 independent mix

### Reverb

Implemented with a `ConvolverNode` driven by a **synthetically generated impulse response** (IR). The IR is built from exponentially-decaying white noise with an early-reflection boost at ~20 ms, simulating a natural room.

The IR is regenerated whenever `reverbDecay` changes; this causes a brief click-free crossfade because the `ConvolverNode` interpolates buffer swaps.

- Decay: 0.1–10 s
- Wet: 0–1

### Distortion

A `WaveShaperNode` with 4× oversampling uses a **soft-clip curve** derived from a Padé approximation of tanh:

```
f(x) = (1 + k/100) · x / (1 + (k/100) · |x|)
```

where `k = amount × 200`. At `k = 0` it passes audio unmodified; at `k = 200` it approaches hard clipping.

A `preGain` node scales input before the shaper so clipping onset matches user expectations across the full range.

---

## Step Sequencer

The sequencer uses the **WebAudio clock** (`AudioContext.currentTime`) for sample-accurate scheduling. A `setInterval` callback fires every 25 ms and schedules any notes that fall within the next 100 ms lookahead window. This design prevents audio glitches caused by JavaScript GC pauses.

```
setInterval (25 ms) ──► schedule()
                           │
                  while nextNoteTime < now + 0.1
                           │
                    scheduleStep(step, time)
                           │
                    channel.noteOn(note, vel, time)  ← AudioContext.currentTime
                           │
                    scheduleNoteOff(...)             ← setTimeout (approx.)
                           │
                    setTimeout(emit('step'), delay)  ← UI highlight
```

**Swing** is applied by adding a fractional delay to every odd-numbered step:

```
swingOffset = (step % 2 === 1) ? stepDuration × swing × 0.33 : 0
```

---

## Song / Pattern Model

```
Song
├── bpm, swing, masterVolume
├── patterns: Pattern[]
│   ├── id, name, stepCount (8/16/32)
│   ├── instruments: InstrumentParams[]   (one per track)
│   └── steps: Step[][]                  [trackIndex][stepIndex]
│       └── { active, note (MIDI), velocity }
└── sequence: string[]   (ordered list of pattern IDs for arrangement)
```

Songs are fully serializable to JSON. The `sequence` array can reference the same pattern ID multiple times, enabling non-destructive looping and arrangement.

---

## WAV Export (Offline Rendering)

The export path creates an `OfflineAudioContext` with the same sample rate as the live context, then rebuilds the full audio graph offline and calls `startRendering()`. The resulting `AudioBuffer` is encoded to **16-bit PCM WAV** in JavaScript (no external codec), then downloaded via a temporary object URL.

The offline render includes a 2-second tail to capture effects decay (delay echoes, reverb ring).

---

## Demo Song: "Neon Pulse"

A four-track techno groove at 128 BPM with two patterns:

| Track | Instrument | Oscillators            | Filter           | Effects           |
|-------|------------|------------------------|------------------|-------------------|
| 0     | Kick       | sine + noise (15%)     | LP @ 200 Hz      | none              |
| 1     | Hi-hat     | noise                  | HP @ 8 kHz, Q=1.5| none              |
| 2     | Bass       | 2× sawtooth (−7 ct)    | LP @ 700 Hz, Q=6 | distortion 30%    |
| 3     | Lead       | square + saw (+1 oct)  | LP @ 3 kHz, Q=3  | delay + reverb    |

**Pattern A** (Main Groove): 4-on-the-floor kick, 8th-note hi-hats, syncopated bass, 8-step lead melody.  
**Pattern B** (Break): Sparse kick (1 and 9 only), quarter-note hats, climbing chromatic lead phrase.

Arrangement: A → A → B → A
