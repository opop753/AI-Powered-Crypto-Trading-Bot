import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

test('successful registration', async () => {
  render(<App />);
  fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: 'testuser' } });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'password' } });
  fireEvent.click(screen.getByText(/Register/i));

  await waitFor(() => {
    expect(screen.getByText(/Registration successful/i)).toBeInTheDocument();
  });
});

test('successful login', async () => {
  render(<App />);
  fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: 'testuser' } });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'password' } });
  fireEvent.click(screen.getByText(/Login/i));

  await waitFor(() => {
    expect(screen.getByText(/Login successful/i)).toBeInTheDocument();
  });
});

test('handles registration error', async () => {
  render(<App />);
  fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: '' } });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'password' } });
  fireEvent.click(screen.getByText(/Register/i));

  await waitFor(() => {
    expect(screen.getByText(/Registration failed/i)).toBeInTheDocument();
  });
});

test('handles login error', async () => {
  render(<App />);
  fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: 'wronguser' } });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'wrongpassword' } });
  fireEvent.click(screen.getByText(/Login/i));

  await waitFor(() => {
    expect(screen.getByText(/Login failed/i)).toBeInTheDocument();
  });
});
