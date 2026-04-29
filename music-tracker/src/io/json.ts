// ─────────────────────────────────────────────────────────────────────────────
// Song persistence: serialize/deserialize Song objects as JSON
// ─────────────────────────────────────────────────────────────────────────────

import type { Song } from '../engine/types';

export function saveSong(song: Song): void {
  const json = JSON.stringify(song, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${song.name.replace(/\s+/g, '_')}.json`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

export function loadSong(file: File): Promise<Song> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const song = JSON.parse(e.target!.result as string) as Song;
        resolve(song);
      } catch {
        reject(new Error('Invalid song file'));
      }
    };
    reader.onerror = () => reject(new Error('Failed to read file'));
    reader.readAsText(file);
  });
}

export function songToLocalStorage(song: Song): void {
  localStorage.setItem('music-tracker-song', JSON.stringify(song));
}

export function songFromLocalStorage(): Song | null {
  const raw = localStorage.getItem('music-tracker-song');
  if (!raw) return null;
  try { return JSON.parse(raw) as Song; } catch { return null; }
}
