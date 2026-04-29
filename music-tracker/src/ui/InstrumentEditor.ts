// ─────────────────────────────────────────────────────────────────────────────
// Instrument editor panel – renders controls for one instrument/track.
// Returns a <details> element that can be collapsed.
// ─────────────────────────────────────────────────────────────────────────────

import type {
  InstrumentParams, AdsrParams, FilterParams, OscillatorParams,
  EffectsParams, OscillatorType,
} from '../engine/types';
import { DEFAULT_OSCILLATOR } from '../engine/types';

type OnChange = (p: InstrumentParams) => void;

function el<K extends keyof HTMLElementTagNameMap>(
  tag: K, cls = '', attrs: Record<string, string> = {},
): HTMLElementTagNameMap[K] {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  return e;
}

function knob(
  label: string,
  value: number,
  min: number,
  max: number,
  step: number,
  onChange: (v: number) => void,
): HTMLElement {
  const wrap = el('div', 'knob-wrap');
  const lbl = el('label', 'knob-label');
  lbl.textContent = label;

  const input = el('input', 'knob-input', {
    type: 'range',
    min: String(min),
    max: String(max),
    step: String(step),
    value: String(value),
  });

  const display = el('span', 'knob-value');
  display.textContent = value.toFixed(step < 1 ? 2 : 0);

  input.addEventListener('input', () => {
    const v = parseFloat(input.value);
    display.textContent = v.toFixed(step < 1 ? 2 : 0);
    onChange(v);
  });

  wrap.append(lbl, input, display);
  return wrap;
}

function select(
  label: string,
  options: string[],
  current: string,
  onChange: (v: string) => void,
): HTMLElement {
  const wrap = el('div', 'select-wrap');
  const lbl = el('label', 'select-label');
  lbl.textContent = label;
  const sel = el('select', 'select-input');
  for (const o of options) {
    const opt = document.createElement('option');
    opt.value = o;
    opt.textContent = o;
    if (o === current) opt.selected = true;
    sel.appendChild(opt);
  }
  sel.addEventListener('change', () => onChange(sel.value));
  wrap.append(lbl, sel);
  return wrap;
}

// ── Sub-sections ──────────────────────────────────────────────────────────

function buildOscSection(
  params: InstrumentParams,
  onChange: OnChange,
): HTMLElement {
  const section = el('div', 'ie-section');
  const title = el('div', 'ie-section-title');
  title.textContent = 'Oscillators';
  section.appendChild(title);

  const oscTypes: OscillatorType[] = ['sine', 'square', 'sawtooth', 'triangle', 'noise'];

  params.oscillators.forEach((osc, idx) => {
    const row = el('div', 'ie-osc-row');
    const label = el('span', 'ie-osc-num');
    label.textContent = `OSC ${idx + 1}`;

    const mutate = (patch: Partial<OscillatorParams>) => {
      params.oscillators[idx] = { ...osc, ...patch };
      osc = params.oscillators[idx];
      onChange({ ...params });
    };

    row.append(
      label,
      select('Type', oscTypes, osc.type, v => mutate({ type: v as OscillatorType })),
      knob('Detune', osc.detune, -1200, 1200, 1, v => mutate({ detune: v })),
      knob('Vol', osc.volume, 0, 1, 0.01, v => mutate({ volume: v })),
    );
    section.appendChild(row);
  });

  // Add/remove oscillator buttons
  const btnRow = el('div', 'ie-btn-row');
  const addBtn = el('button', 'ie-btn');
  addBtn.textContent = '+ OSC';
  addBtn.addEventListener('click', () => {
    if (params.oscillators.length < 3) {
      params.oscillators.push({ ...DEFAULT_OSCILLATOR });
      onChange({ ...params });
    }
  });
  const remBtn = el('button', 'ie-btn danger');
  remBtn.textContent = '− OSC';
  remBtn.addEventListener('click', () => {
    if (params.oscillators.length > 1) {
      params.oscillators.pop();
      onChange({ ...params });
    }
  });
  btnRow.append(addBtn, remBtn);
  section.appendChild(btnRow);
  return section;
}

function buildAdsrSection(params: InstrumentParams, onChange: OnChange): HTMLElement {
  const section = el('div', 'ie-section');
  const title = el('div', 'ie-section-title');
  title.textContent = 'ADSR Envelope';
  section.appendChild(title);

  const row = el('div', 'ie-row');
  const mutate = (patch: Partial<AdsrParams>) => {
    params.adsr = { ...params.adsr, ...patch };
    onChange({ ...params });
  };

  row.append(
    knob('A', params.adsr.attack, 0.001, 4, 0.001, v => mutate({ attack: v })),
    knob('D', params.adsr.decay, 0.001, 4, 0.001, v => mutate({ decay: v })),
    knob('S', params.adsr.sustain, 0, 1, 0.01, v => mutate({ sustain: v })),
    knob('R', params.adsr.release, 0.001, 8, 0.001, v => mutate({ release: v })),
  );
  section.appendChild(row);
  return section;
}

function buildFilterSection(params: InstrumentParams, onChange: OnChange): HTMLElement {
  const section = el('div', 'ie-section');
  const title = el('div', 'ie-section-title');
  title.textContent = 'Filter';
  section.appendChild(title);

  const row = el('div', 'ie-row');
  const filterTypes: BiquadFilterType[] = [
    'lowpass', 'highpass', 'bandpass', 'notch', 'peaking', 'allpass',
  ];
  const mutate = (patch: Partial<FilterParams>) => {
    params.filter = { ...params.filter, ...patch };
    onChange({ ...params });
  };

  row.append(
    select('Type', filterTypes, params.filter.type, v => mutate({ type: v as BiquadFilterType })),
    knob('Freq', params.filter.frequency, 20, 20000, 1, v => mutate({ frequency: v })),
    knob('Q', params.filter.Q, 0.001, 30, 0.001, v => mutate({ Q: v })),
    knob('Gain', params.filter.gain, -24, 24, 0.1, v => mutate({ gain: v })),
  );
  section.appendChild(row);
  return section;
}

function buildEffectsSection(params: InstrumentParams, onChange: OnChange): HTMLElement {
  const section = el('div', 'ie-section');
  const title = el('div', 'ie-section-title');
  title.textContent = 'Effects';
  section.appendChild(title);

  const mutate = (patch: Partial<EffectsParams>) => {
    params.effects = { ...params.effects, ...patch };
    onChange({ ...params });
  };

  const delayRow = el('div', 'ie-row');
  const delayTitle = el('div', 'ie-subsection-title');
  delayTitle.textContent = 'Delay';
  delayRow.append(
    delayTitle,
    knob('Time', params.effects.delayTime, 0, 1, 0.001, v => mutate({ delayTime: v })),
    knob('FB', params.effects.delayFeedback, 0, 0.95, 0.01, v => mutate({ delayFeedback: v })),
    knob('Wet', params.effects.delayWet, 0, 1, 0.01, v => mutate({ delayWet: v })),
  );

  const revRow = el('div', 'ie-row');
  const revTitle = el('div', 'ie-subsection-title');
  revTitle.textContent = 'Reverb';
  revRow.append(
    revTitle,
    knob('Decay', params.effects.reverbDecay, 0.1, 10, 0.1, v => mutate({ reverbDecay: v })),
    knob('Wet', params.effects.reverbWet, 0, 1, 0.01, v => mutate({ reverbWet: v })),
  );

  const distRow = el('div', 'ie-row');
  const distTitle = el('div', 'ie-subsection-title');
  distTitle.textContent = 'Distortion';
  distRow.append(
    distTitle,
    knob('Amount', params.effects.distortionAmount, 0, 1, 0.01, v => mutate({ distortionAmount: v })),
    knob('Wet', params.effects.distortionWet, 0, 1, 0.01, v => mutate({ distortionWet: v })),
  );

  section.append(delayRow, revRow, distRow);
  return section;
}

function buildChannelSection(params: InstrumentParams, onChange: OnChange): HTMLElement {
  const section = el('div', 'ie-section');
  const title = el('div', 'ie-section-title');
  title.textContent = 'Channel';
  section.appendChild(title);

  const row = el('div', 'ie-row');
  row.append(
    knob('Vol', params.volume, 0, 1, 0.01, v => { params.volume = v; onChange({ ...params }); }),
    knob('Pan', params.pan, -1, 1, 0.01, v => { params.pan = v; onChange({ ...params }); }),
  );
  section.appendChild(row);
  return section;
}

// ── Public factory ─────────────────────────────────────────────────────────

export function buildInstrumentEditor(
  params: InstrumentParams,
  onChange: OnChange,
): HTMLElement {
  const details = el('details', 'instrument-editor');
  const summary = el('summary', 'ie-summary');
  summary.textContent = params.name;
  details.appendChild(summary);

  const rebuild = () => {
    // Remove old sections (keep summary)
    while (details.children.length > 1) details.removeChild(details.lastChild!);

    const newOnChange: OnChange = (p) => {
      // Update summary name if changed
      summary.textContent = p.name;
      onChange(p);
      // Re-render to reflect structural changes (osc count)
      rebuild();
    };

    details.append(
      buildChannelSection(params, newOnChange),
      buildOscSection(params, newOnChange),
      buildAdsrSection(params, newOnChange),
      buildFilterSection(params, newOnChange),
      buildEffectsSection(params, newOnChange),
    );
  };

  rebuild();
  return details;
}
