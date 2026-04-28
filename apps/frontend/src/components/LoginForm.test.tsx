import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('calls login handler in login mode', () => {
    const onLogin = vi.fn().mockResolvedValue(undefined);
    render(
      <LoginForm
        onLogin={onLogin}
        onRegister={vi.fn().mockResolvedValue(undefined)}
        onOAuth={vi.fn().mockResolvedValue(undefined)}
      />,
    );

    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'user@example.com' },
    });
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'Password123!' },
    });
    fireEvent.click(screen.getByText('Sign in'));

    expect(onLogin).toHaveBeenCalledWith({
      email: 'user@example.com',
      password: 'Password123!',
    });
  });

  it('shows register fields and calls register handler', () => {
    const onRegister = vi.fn().mockResolvedValue(undefined);
    render(
      <LoginForm
        onLogin={vi.fn().mockResolvedValue(undefined)}
        onRegister={onRegister}
        onOAuth={vi.fn().mockResolvedValue(undefined)}
      />,
    );

    fireEvent.click(screen.getByText('Register'));
    fireEvent.change(screen.getByPlaceholderText('Name'), {
      target: { value: 'Jane' },
    });
    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'jane@example.com' },
    });
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'Password123!' },
    });
    fireEvent.click(screen.getByText('Create account'));

    expect(onRegister).toHaveBeenCalledWith({
      name: 'Jane',
      email: 'jane@example.com',
      password: 'Password123!',
    });
  });
});
