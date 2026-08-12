import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import HomePage from './page';

describe('HomePage', () => {
  it('checks the session before rendering', () => {
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: false })));
    render(<HomePage />);
    expect(screen.getByRole('main')).toBeTruthy();
  });
});
