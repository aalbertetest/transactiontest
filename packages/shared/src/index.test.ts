import { describe, expect, it } from 'vitest';
import { formatCurrency, isPlanId, plans } from './index';

describe('shared plan utilities', () => {
  it('formats plan prices', () => {
    expect(formatCurrency(plans[0].monthlyPriceCents)).toBe('$19.00');
  });

  it('validates known plan identifiers', () => {
    expect(isPlanId('growth')).toBe(true);
    expect(isPlanId('enterprise')).toBe(false);
  });
});
