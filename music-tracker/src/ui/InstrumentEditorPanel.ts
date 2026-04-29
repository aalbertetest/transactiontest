// ─────────────────────────────────────────────────────────────────────────────
// Instrument editor panel – shows per-track instrument editors in a tabbed view
// ─────────────────────────────────────────────────────────────────────────────

import type { Pattern, InstrumentParams } from '../engine/types';
import { buildInstrumentEditor } from './InstrumentEditor';

type OnInstrumentChange = (trackIdx: number, params: InstrumentParams) => void;

export class InstrumentEditor {
  private container: HTMLElement;
  private pattern: Pattern;
  private onChange: OnInstrumentChange;
  private activeTrack = 0;

  constructor(
    container: HTMLElement,
    pattern: Pattern,
    onChange: OnInstrumentChange,
  ) {
    this.container = container;
    this.pattern = pattern;
    this.onChange = onChange;
    this.render();
  }

  render(): void {
    this.container.innerHTML = '';

    const header = document.createElement('div');
    header.className = 'ie-panel-header';
    const title = document.createElement('div');
    title.className = 'ie-panel-title';
    title.textContent = 'Instruments';
    header.appendChild(title);

    // Tab row
    const tabs = document.createElement('div');
    tabs.className = 'ie-tabs';

    this.pattern.instruments.forEach((inst, idx) => {
      const tab = document.createElement('button');
      tab.className = `ie-tab${idx === this.activeTrack ? ' active' : ''}`;
      tab.textContent = inst.name;
      tab.addEventListener('click', () => {
        this.activeTrack = idx;
        this.render();
      });
      tabs.appendChild(tab);
    });

    const body = document.createElement('div');
    body.className = 'ie-panel-body';

    const activeParams = this.pattern.instruments[this.activeTrack];
    if (activeParams) {
      const editor = buildInstrumentEditor(
        JSON.parse(JSON.stringify(activeParams)), // work on a copy
        (updated) => {
          this.pattern.instruments[this.activeTrack] = updated;
          // Update tab label
          tabs.children[this.activeTrack].textContent = updated.name;
          this.onChange(this.activeTrack, updated);
        },
      );
      (editor as HTMLDetailsElement).open = true;
      body.appendChild(editor);
    }

    this.container.append(header, tabs, body);
  }

  updatePattern(pattern: Pattern): void {
    this.pattern = pattern;
    this.activeTrack = 0;
    this.render();
  }
}
