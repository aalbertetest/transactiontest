import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { App } from './App';

vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve([]) })));

describe('App', () => {
  it('renders the landing page', () => {
    render(<App />);
    expect(screen.getByText(/Launch-ready monorepo/i)).toBeInTheDocument();
  });
});
