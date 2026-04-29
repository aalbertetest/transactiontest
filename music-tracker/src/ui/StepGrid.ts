// ─────────────────────────────────────────────────────────────────────────────
// Step sequencer grid – renders a matrix of step buttons for all tracks.
// Supports:
//   • Left-click  → toggle step on/off
//   • Right-click → open per-step note/velocity editor
//   • Highlight current playhead position
// ─────────────────────────────────────────────────────────────────────────────

import type { Pattern, Step } from '../engine/types';
import { midiToName } from '../engine/types';

export type OnStepChange = (trackIdx: number, stepIdx: number, step: Step) => void;
export type OnPreviewNote = (trackIdx: number, midi: number) => void;

export class StepGrid {
  private container: HTMLElement;
  private pattern: Pattern;
  private onStepChange: OnStepChange;
  private onPreview: OnPreviewNote;
  private cells: HTMLButtonElement[][][] = []; // [track][step]
  private currentStep = -1;
  private notePopup: HTMLElement | null = null;

  constructor(
    container: HTMLElement,
    pattern: Pattern,
    onStepChange: OnStepChange,
    onPreview: OnPreviewNote,
  ) {
    this.container = container;
    this.pattern = pattern;
    this.onStepChange = onStepChange;
    this.onPreview = onPreview;
    this.render();
  }

  render(): void {
    this.container.innerHTML = '';
    this.cells = [];

    const grid = document.createElement('div');
    grid.className = 'step-grid';
    grid.style.setProperty('--step-count', String(this.pattern.stepCount));

    // Step number header
    const header = document.createElement('div');
    header.className = 'step-header';

    // track-label placeholder
    const tl = document.createElement('div');
    tl.className = 'track-label-cell';
    header.appendChild(tl);

    for (let s = 0; s < this.pattern.stepCount; s++) {
      const num = document.createElement('div');
      num.className = 'step-num';
      // Show beat markers (every 4 steps)
      num.textContent = s % 4 === 0 ? String(s / 4 + 1) : '';
      if (s % 4 === 0) num.classList.add('beat-marker');
      header.appendChild(num);
    }
    grid.appendChild(header);

    // Track rows
    for (let t = 0; t < this.pattern.instruments.length; t++) {
      const trackCells: HTMLButtonElement[] = [];
      const row = document.createElement('div');
      row.className = 'step-row';

      const label = document.createElement('div');
      label.className = 'track-label';
      label.textContent = this.pattern.instruments[t].name;
      label.title = `Preview ${this.pattern.instruments[t].name}`;
      label.addEventListener('click', () => {
        const step = this.pattern.steps[t]?.find(s => s.active);
        this.onPreview(t, step?.note ?? 60);
      });
      row.appendChild(label);

      for (let s = 0; s < this.pattern.stepCount; s++) {
        const step = this.pattern.steps[t]?.[s] ?? { active: false, note: 60, velocity: 0.8 };
        const btn = document.createElement('button');
        btn.className = this.cellClass(step, s);
        btn.dataset.track = String(t);
        btn.dataset.step = String(s);

        btn.addEventListener('click', () => this.toggleStep(t, s));
        btn.addEventListener('contextmenu', (e) => {
          e.preventDefault();
          this.openNoteEditor(t, s, btn);
        });

        row.appendChild(btn);
        trackCells.push(btn);
      }

      this.cells.push([trackCells]);
      grid.appendChild(row);
    }

    this.container.appendChild(grid);
    if (this.currentStep >= 0) this.highlightStep(this.currentStep);
  }

  private cellClass(step: Step, stepIdx: number): string {
    const classes = ['step-btn'];
    if (step.active) classes.push('active');
    if (stepIdx % 4 === 0) classes.push('beat-start');
    else if (stepIdx % 2 === 0) classes.push('half-beat');
    return classes.join(' ');
  }

  private toggleStep(trackIdx: number, stepIdx: number): void {
    const step = this.pattern.steps[trackIdx]?.[stepIdx];
    if (!step) return;
    step.active = !step.active;
    const btn = this.cells[trackIdx]?.[0]?.[stepIdx];
    if (btn) btn.className = this.cellClass(step, stepIdx);
    this.onStepChange(trackIdx, stepIdx, { ...step });
  }

  highlightStep(step: number): void {
    // Clear previous
    if (this.currentStep >= 0) {
      for (let t = 0; t < this.cells.length; t++) {
        const btn = this.cells[t]?.[0]?.[this.currentStep];
        if (btn) btn.classList.remove('playing');
      }
    }
    this.currentStep = step;
    for (let t = 0; t < this.cells.length; t++) {
      const btn = this.cells[t]?.[0]?.[step];
      if (btn) btn.classList.add('playing');
    }
  }

  clearHighlight(): void {
    if (this.currentStep >= 0) {
      for (let t = 0; t < this.cells.length; t++) {
        this.cells[t]?.[0]?.[this.currentStep]?.classList.remove('playing');
      }
      this.currentStep = -1;
    }
  }

  // ── Per-step note/velocity popup ─────────────────────────────────────────

  private openNoteEditor(trackIdx: number, stepIdx: number, anchor: HTMLElement): void {
    this.closeNoteEditor();

    const step = this.pattern.steps[trackIdx]?.[stepIdx];
    if (!step) return;

    const popup = document.createElement('div');
    popup.className = 'note-popup';

    // Note selector (octave + note name)
    const noteRow = document.createElement('div');
    noteRow.className = 'note-popup-row';
    const noteLbl = document.createElement('label');
    noteLbl.textContent = 'Note';

    const noteSelect = document.createElement('select');
    for (let midi = 21; midi <= 108; midi++) {
      const opt = document.createElement('option');
      opt.value = String(midi);
      opt.textContent = midiToName(midi);
      if (midi === step.note) opt.selected = true;
      noteSelect.appendChild(opt);
    }
    noteSelect.addEventListener('change', () => {
      step.note = parseInt(noteSelect.value);
      this.onStepChange(trackIdx, stepIdx, { ...step });
      this.onPreview(trackIdx, step.note);
    });

    noteRow.append(noteLbl, noteSelect);

    // Velocity slider
    const velRow = document.createElement('div');
    velRow.className = 'note-popup-row';
    const velLbl = document.createElement('label');
    velLbl.textContent = 'Velocity';
    const velInput = document.createElement('input');
    velInput.type = 'range';
    velInput.min = '0';
    velInput.max = '1';
    velInput.step = '0.01';
    velInput.value = String(step.velocity);
    const velDisplay = document.createElement('span');
    velDisplay.textContent = step.velocity.toFixed(2);
    velInput.addEventListener('input', () => {
      step.velocity = parseFloat(velInput.value);
      velDisplay.textContent = step.velocity.toFixed(2);
      this.onStepChange(trackIdx, stepIdx, { ...step });
    });
    velRow.append(velLbl, velInput, velDisplay);

    // Close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'note-popup-close';
    closeBtn.textContent = '✕';
    closeBtn.addEventListener('click', () => this.closeNoteEditor());

    popup.append(noteRow, velRow, closeBtn);

    // Position near anchor
    const rect = anchor.getBoundingClientRect();
    popup.style.position = 'fixed';
    popup.style.top = `${rect.bottom + 4}px`;
    popup.style.left = `${rect.left}px`;

    document.body.appendChild(popup);
    this.notePopup = popup;

    // Close on outside click
    const outside = (e: MouseEvent) => {
      if (!popup.contains(e.target as Node) && e.target !== anchor) {
        this.closeNoteEditor();
        document.removeEventListener('mousedown', outside);
      }
    };
    setTimeout(() => document.addEventListener('mousedown', outside), 10);
  }

  private closeNoteEditor(): void {
    this.notePopup?.remove();
    this.notePopup = null;
  }

  updatePattern(pattern: Pattern): void {
    this.pattern = pattern;
    this.render();
  }
}
