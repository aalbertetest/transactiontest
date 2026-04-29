// ─────────────────────────────────────────────────────────────────────────────
// Pattern Manager – list of patterns and the song sequence arrangement
// ─────────────────────────────────────────────────────────────────────────────

import type { Song, Pattern, Step, InstrumentParams } from '../engine/types';
import { DEFAULT_ADSR, DEFAULT_EFFECTS, DEFAULT_FILTER, DEFAULT_OSCILLATOR } from '../engine/types';

function uid(): string {
  return `p-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;
}

function emptyPattern(trackCount: number, stepCount = 16): Pattern {
  return {
    id: uid(),
    name: 'New Pattern',
    stepCount,
    steps: Array.from({ length: trackCount }, () =>
      Array.from({ length: stepCount }, (): Step => ({ active: false, note: 60, velocity: 0.8 }))
    ),
    instruments: Array.from({ length: trackCount }, (_, i) => defaultInstrument(i)),
  };
}

function defaultInstrument(idx: number): InstrumentParams {
  const names = ['Kick', 'Hi-hat', 'Bass', 'Lead', 'Pad', 'Arp', 'FX', 'Perc'];
  return {
    name: names[idx % names.length],
    oscillators: [{ ...DEFAULT_OSCILLATOR }],
    adsr: { ...DEFAULT_ADSR },
    filter: { ...DEFAULT_FILTER },
    effects: { ...DEFAULT_EFFECTS },
    volume: 0.7,
    pan: 0,
  };
}

export type OnPatternSelect = (pattern: Pattern, index: number) => void;
export type OnSongChange = (song: Song) => void;

export class PatternManager {
  private container: HTMLElement;
  private song: Song;
  private onSelect: OnPatternSelect;
  private onSongChange: OnSongChange;
  private selectedIdx = 0;

  constructor(
    container: HTMLElement,
    song: Song,
    onSelect: OnPatternSelect,
    onSongChange: OnSongChange,
  ) {
    this.container = container;
    this.song = song;
    this.onSelect = onSelect;
    this.onSongChange = onSongChange;
    this.render();
  }

  render(): void {
    this.container.innerHTML = '';

    const title = document.createElement('div');
    title.className = 'pm-title';
    title.textContent = 'Patterns';

    const list = document.createElement('div');
    list.className = 'pm-list';

    this.song.patterns.forEach((pat, idx) => {
      const row = document.createElement('div');
      row.className = `pm-row${idx === this.selectedIdx ? ' selected' : ''}`;

      const name = document.createElement('input');
      name.className = 'pm-name-input';
      name.value = pat.name;
      name.addEventListener('change', () => {
        pat.name = name.value;
        this.onSongChange(this.song);
      });

      const dupBtn = document.createElement('button');
      dupBtn.className = 'pm-btn';
      dupBtn.title = 'Duplicate';
      dupBtn.textContent = '⧉';
      dupBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const clone = JSON.parse(JSON.stringify(pat)) as Pattern;
        clone.id = uid();
        clone.name = pat.name + ' Copy';
        this.song.patterns.splice(idx + 1, 0, clone);
        this.onSongChange(this.song);
        this.render();
      });

      const delBtn = document.createElement('button');
      delBtn.className = 'pm-btn danger';
      delBtn.title = 'Delete';
      delBtn.textContent = '✕';
      delBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.song.patterns.length <= 1) return;
        this.song.patterns.splice(idx, 1);
        this.song.sequence = this.song.sequence.filter(id => id !== pat.id);
        if (this.selectedIdx >= this.song.patterns.length) this.selectedIdx = 0;
        this.onSongChange(this.song);
        this.onSelect(this.song.patterns[this.selectedIdx], this.selectedIdx);
        this.render();
      });

      row.append(name, dupBtn, delBtn);
      row.addEventListener('click', () => {
        this.selectedIdx = idx;
        this.onSelect(pat, idx);
        this.render();
      });

      list.appendChild(row);
    });

    const addBtn = document.createElement('button');
    addBtn.className = 'pm-add-btn';
    addBtn.textContent = '+ Pattern';
    addBtn.addEventListener('click', () => {
      const trackCount = this.song.patterns[0]?.instruments.length ?? 4;
      const pat = emptyPattern(trackCount);
      this.song.patterns.push(pat);
      this.selectedIdx = this.song.patterns.length - 1;
      this.onSongChange(this.song);
      this.onSelect(pat, this.selectedIdx);
      this.render();
    });

    // Sequence arrangement
    const seqTitle = document.createElement('div');
    seqTitle.className = 'pm-title';
    seqTitle.textContent = 'Arrangement';

    const seqList = document.createElement('div');
    seqList.className = 'pm-seq-list';

    this.song.sequence.forEach((pid, seqIdx) => {
      const pat = this.song.patterns.find(p => p.id === pid);
      const chip = document.createElement('div');
      chip.className = 'pm-seq-chip';
      chip.textContent = pat?.name ?? '?';
      chip.title = 'Click to remove from sequence';
      chip.addEventListener('click', () => {
        this.song.sequence.splice(seqIdx, 1);
        this.onSongChange(this.song);
        this.render();
      });
      seqList.appendChild(chip);
    });

    const seqAddRow = document.createElement('div');
    seqAddRow.className = 'pm-seq-add-row';
    const seqSel = document.createElement('select');
    seqSel.className = 'pm-seq-select';
    this.song.patterns.forEach(pat => {
      const opt = document.createElement('option');
      opt.value = pat.id;
      opt.textContent = pat.name;
      seqSel.appendChild(opt);
    });
    const seqAddBtn = document.createElement('button');
    seqAddBtn.className = 'pm-btn';
    seqAddBtn.textContent = '+ Add to seq';
    seqAddBtn.addEventListener('click', () => {
      this.song.sequence.push(seqSel.value);
      this.onSongChange(this.song);
      this.render();
    });
    seqAddRow.append(seqSel, seqAddBtn);

    this.container.append(title, list, addBtn, seqTitle, seqList, seqAddRow);
  }

  updateSong(song: Song): void {
    this.song = song;
    this.render();
  }
}
