// ─────────────────────────────────────────────────────────────────────────────
// Main application controller
// ─────────────────────────────────────────────────────────────────────────────

import { Sequencer } from '../engine/sequencer';
import type { Song, Pattern } from '../engine/types';
import { DEMO_SONG } from '../io/demo-song';
import { saveSong, loadSong, songToLocalStorage, songFromLocalStorage } from '../io/json';
import { downloadWav } from '../io/wav';
import { StepGrid } from './StepGrid';
import { InstrumentEditor } from './InstrumentEditorPanel';
import { PatternManager } from './PatternManager';

export class App {
  private ctx: AudioContext;
  private seq: Sequencer;
  private song: Song;
  private activePattern: Pattern;
  private stepGrid: StepGrid | null = null;
  private _instrPanel: InstrumentEditor | null = null;
  private _patternMgr: PatternManager | null = null;
  private bpmInput!: HTMLInputElement;
  private swingInput!: HTMLInputElement;
  private masterVolInput!: HTMLInputElement;
  private playBtn!: HTMLButtonElement;
  private exportBtn!: HTMLButtonElement;
  private isRendering = false;

  constructor() {
    this.ctx = new AudioContext();
    this.seq = new Sequencer(this.ctx);
    this.song = songFromLocalStorage() ?? JSON.parse(JSON.stringify(DEMO_SONG));
    this.activePattern = this.song.patterns[0];
    this.seq.loadSong(this.song);
  }

  mount(root: HTMLElement): void {
    root.innerHTML = this.buildShell();
    this.bindElements(root);
    this.buildGridArea(root);
    this.buildSidebar(root);
    this.buildInstrPanel(root);

    // Sequencer step listener
    this.seq.on((e) => {
      if (e.type === 'step' && e.step !== undefined) {
        this.stepGrid?.highlightStep(e.step);
      }
      if (e.type === 'stop') {
        this.stepGrid?.clearHighlight();
        this.playBtn.textContent = '▶ Play';
        this.playBtn.classList.remove('playing');
      }
      if (e.type === 'patternChange' && e.patternIndex !== undefined) {
        const pid = this.song.sequence[e.patternIndex];
        const pat = this.song.patterns.find(p => p.id === pid);
        if (pat) this.switchPattern(pat);
      }
    });
  }

  private buildShell(): string {
    return `
      <header class="app-header">
        <div class="app-logo">🎹 Music Tracker</div>
        <div class="transport-bar" id="transport"></div>
        <div class="header-actions" id="header-actions"></div>
      </header>
      <main class="app-main">
        <aside class="sidebar" id="sidebar"></aside>
        <div class="workspace">
          <div class="grid-area" id="grid-area"></div>
          <div class="instr-panel" id="instr-panel"></div>
        </div>
      </main>
      <div class="statusbar" id="statusbar">Ready</div>
    `;
  }

  private bindElements(root: HTMLElement): void {
    const transport = root.querySelector('#transport')!;
    const headerActions = root.querySelector('#header-actions')!;

    // Play/Stop
    this.playBtn = document.createElement('button');
    this.playBtn.className = 'transport-btn play-btn';
    this.playBtn.textContent = '▶ Play';
    this.playBtn.addEventListener('click', () => this.togglePlay());

    // BPM
    const bpmWrap = document.createElement('div');
    bpmWrap.className = 'transport-group';
    const bpmLbl = document.createElement('label');
    bpmLbl.textContent = 'BPM';
    this.bpmInput = document.createElement('input');
    this.bpmInput.type = 'number';
    this.bpmInput.className = 'transport-input';
    this.bpmInput.min = '40';
    this.bpmInput.max = '300';
    this.bpmInput.value = String(this.song.bpm);
    this.bpmInput.addEventListener('change', () => {
      this.song.bpm = clamp(parseInt(this.bpmInput.value), 40, 300);
      this.bpmInput.value = String(this.song.bpm);
      this.autosave();
    });
    bpmWrap.append(bpmLbl, this.bpmInput);

    // Swing
    const swingWrap = document.createElement('div');
    swingWrap.className = 'transport-group';
    const swingLbl = document.createElement('label');
    swingLbl.textContent = 'Swing';
    this.swingInput = document.createElement('input');
    this.swingInput.type = 'range';
    this.swingInput.className = 'transport-slider';
    this.swingInput.min = '0';
    this.swingInput.max = '1';
    this.swingInput.step = '0.01';
    this.swingInput.value = String(this.song.swing);
    this.swingInput.addEventListener('input', () => {
      this.song.swing = parseFloat(this.swingInput.value);
      this.autosave();
    });
    swingWrap.append(swingLbl, this.swingInput);

    // Master volume
    const volWrap = document.createElement('div');
    volWrap.className = 'transport-group';
    const volLbl = document.createElement('label');
    volLbl.textContent = 'Master';
    this.masterVolInput = document.createElement('input');
    this.masterVolInput.type = 'range';
    this.masterVolInput.className = 'transport-slider';
    this.masterVolInput.min = '0';
    this.masterVolInput.max = '1';
    this.masterVolInput.step = '0.01';
    this.masterVolInput.value = String(this.song.masterVolume);
    this.masterVolInput.addEventListener('input', () => {
      this.song.masterVolume = parseFloat(this.masterVolInput.value);
      this.seq.master.gain.value = this.song.masterVolume;
      this.autosave();
    });
    volWrap.append(volLbl, this.masterVolInput);

    transport.append(this.playBtn, bpmWrap, swingWrap, volWrap);

    // Song name
    const songNameInput = document.createElement('input');
    songNameInput.className = 'song-name-input';
    songNameInput.value = this.song.name;
    songNameInput.placeholder = 'Song name…';
    songNameInput.addEventListener('change', () => {
      this.song.name = songNameInput.value;
      this.autosave();
    });

    // Save JSON
    const saveBtn = document.createElement('button');
    saveBtn.className = 'header-btn';
    saveBtn.textContent = '💾 Save';
    saveBtn.addEventListener('click', () => saveSong(this.song));

    // Load JSON
    const loadInput = document.createElement('input');
    loadInput.type = 'file';
    loadInput.accept = '.json';
    loadInput.style.display = 'none';
    loadInput.addEventListener('change', async () => {
      if (!loadInput.files?.[0]) return;
      try {
        const loaded = await loadSong(loadInput.files[0]);
        this.song = loaded;
        this.activePattern = loaded.patterns[0];
        this.seq.loadSong(loaded);
        this.buildGridArea(root);
        this.buildSidebar(root);
        this.buildInstrPanel(root);
        this.setStatus('Song loaded ✓');
        this.autosave();
      } catch (e) {
        this.setStatus('Failed to load song');
      }
    });

    const loadBtn = document.createElement('button');
    loadBtn.className = 'header-btn';
    loadBtn.textContent = '📂 Open';
    loadBtn.addEventListener('click', () => loadInput.click());

    // Demo song
    const demoBtn = document.createElement('button');
    demoBtn.className = 'header-btn';
    demoBtn.textContent = '🎵 Demo';
    demoBtn.addEventListener('click', () => {
      this.song = JSON.parse(JSON.stringify(DEMO_SONG));
      this.activePattern = this.song.patterns[0];
      this.seq.loadSong(this.song);
      this.buildGridArea(root);
      this.buildSidebar(root);
      this.buildInstrPanel(root);
      this.setStatus('Demo song loaded');
    });

    // Export WAV
    this.exportBtn = document.createElement('button');
    this.exportBtn.className = 'header-btn';
    this.exportBtn.textContent = '⬇ WAV';
    this.exportBtn.addEventListener('click', () => this.exportWav());

    headerActions.append(songNameInput, demoBtn, loadBtn, saveBtn, this.exportBtn, loadInput);
  }

  private buildGridArea(root: HTMLElement): void {
    const area = root.querySelector('#grid-area')!;
    area.innerHTML = '';

    // Step count selector
    const topBar = document.createElement('div');
    topBar.className = 'grid-topbar';

    const stepCountLabel = document.createElement('span');
    stepCountLabel.textContent = 'Steps:';
    topBar.appendChild(stepCountLabel);

    [8, 16, 32].forEach(n => {
      const btn = document.createElement('button');
      btn.className = `step-count-btn${this.activePattern.stepCount === n ? ' active' : ''}`;
      btn.textContent = String(n);
      btn.addEventListener('click', () => {
        this.activePattern.stepCount = n;
        // Resize steps arrays
        for (let t = 0; t < this.activePattern.instruments.length; t++) {
          const cur = this.activePattern.steps[t] ?? [];
          while (cur.length < n) cur.push({ active: false, note: 60, velocity: 0.8 });
          this.activePattern.steps[t] = cur.slice(0, n);
        }
        this.autosave();
        this.buildGridArea(root);
      });
      topBar.appendChild(btn);
    });

    area.appendChild(topBar);

    const gridContainer = document.createElement('div');
    gridContainer.className = 'grid-container';
    area.appendChild(gridContainer);

    this.stepGrid = new StepGrid(
      gridContainer,
      this.activePattern,
      (trackIdx, stepIdx, step) => {
        this.activePattern.steps[trackIdx][stepIdx] = step;
        this.autosave();
      },
      (trackIdx, midi) => this.seq.previewNote(trackIdx, midi),
    );
  }

  private buildSidebar(root: HTMLElement): void {
    const sidebar = root.querySelector('#sidebar')!;
    sidebar.innerHTML = '';

    this._patternMgr = new PatternManager(
      sidebar as HTMLElement,
      this.song,
      (pat) => {
        this.switchPattern(pat);
        this.buildInstrPanel(root);
      },
      (song) => {
        this.song = song;
        this.autosave();
      },
    );
  }

  private buildInstrPanel(root: HTMLElement): void {
    const panel = root.querySelector('#instr-panel')!;
    panel.innerHTML = '';

    this._instrPanel = new InstrumentEditor(
      panel as HTMLElement,
      this.activePattern,
      (trackIdx, params) => {
        this.activePattern.instruments[trackIdx] = params;
        this.seq.updateInstrument(trackIdx, params);
        this.autosave();
      },
    );
  }

  private switchPattern(pat: Pattern): void {
    this.activePattern = pat;
    this.seq.loadPattern(pat);

    // Rebuild grid with new pattern (find root element)
    const root = document.querySelector('#app')!;
    this.buildGridArea(root as HTMLElement);
  }

  private togglePlay(): void {
    if (this.ctx.state === 'suspended') this.ctx.resume();
    this.seq.toggle();
    if (this.seq.playing) {
      this.playBtn.textContent = '■ Stop';
      this.playBtn.classList.add('playing');
      this.setStatus('Playing…');
    } else {
      this.playBtn.textContent = '▶ Play';
      this.playBtn.classList.remove('playing');
      this.stepGrid?.clearHighlight();
      this.setStatus('Stopped');
    }
  }

  private async exportWav(): Promise<void> {
    if (this.isRendering) return;
    this.isRendering = true;
    this.exportBtn.disabled = true;
    this.exportBtn.textContent = '⏳ Rendering…';
    this.setStatus('Rendering WAV… (this may take a moment)');
    try {
      const buf = await this.seq.renderToBuffer(this.song);
      downloadWav(buf, `${this.song.name.replace(/\s+/g, '_')}.wav`);
      this.setStatus('WAV exported ✓');
    } catch (e) {
      this.setStatus(`Export failed: ${e}`);
    } finally {
      this.isRendering = false;
      this.exportBtn.disabled = false;
      this.exportBtn.textContent = '⬇ WAV';
    }
  }

  private autosave(): void {
    songToLocalStorage(this.song);
  }

  private setStatus(msg: string): void {
    const bar = document.querySelector('#statusbar');
    if (bar) bar.textContent = msg;
  }
}

function clamp(v: number, lo: number, hi: number): number {
  return Math.max(lo, Math.min(hi, v));
}
