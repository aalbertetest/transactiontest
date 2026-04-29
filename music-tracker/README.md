# Music Tracker

A browser-based step sequencer and synthesizer built with **TypeScript** and the **Web Audio API** — no plugins, no WASM, no server.

## Features

- **Step sequencer** – 8, 16, or 32 steps per pattern; per-step note and velocity editing
- **Multi-oscillator synth** – up to 3 oscillators per track (sine, square, sawtooth, triangle, noise)
- **ADSR envelope** – attack, decay, sustain, release per instrument
- **Resonant filter** – lowpass, highpass, bandpass, notch, peaking, allpass
- **Effects chain** – delay, convolution reverb, waveshaper distortion (all with wet/dry blend)
- **Pattern manager** – create, duplicate, delete patterns; arrange in a song sequence
- **WAV export** – offline render entire song to 16-bit PCM WAV
- **Save / Load** – songs serialized as JSON; autosaved to localStorage
- **Demo song** – "Neon Pulse" loaded on first launch

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in a modern browser (Chrome, Firefox, Safari 15+, Edge).

## Building

```bash
npm run build
```

Output goes to `dist/`. Serve with any static file server.

## Usage

| Control | Action |
|---------|--------|
| **▶ Play** | Start sequencer; becomes **■ Stop** while playing |
| **BPM** | Tempo (40–300); affects playback and WAV export |
| **Swing** | Shuffle amount applied to odd steps |
| **Master** | Master output volume |
| Click step button | Toggle step on/off |
| Right-click step | Open note & velocity editor |
| Click track label | Preview the track sound |
| **+ Pattern** | Add a blank pattern |
| Pattern name | Click to select; edit to rename |
| ⧉ button | Duplicate pattern |
| ✕ button | Delete pattern |
| Arrangement chips | Add patterns to song sequence; click chip to remove |
| **💾 Save** | Download song as JSON |
| **📂 Open** | Load song from JSON file |
| **🎵 Demo** | Reset to built-in demo song |
| **⬇ WAV** | Render and download full song as WAV |

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for a detailed description of the synth signal chain, scheduler design, effects implementation, and data model.

## Tech Stack

- [Vite](https://vitejs.dev/) – build tooling
- [TypeScript](https://www.typescriptlang.org/) – type safety
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) – all audio processing
