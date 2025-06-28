import { User, UserRole } from '../types/user';

const API_URL = '/api';

export async function signup(
  email: string,
  password: string,
  name: string,
  role: UserRole
) {
  const res = await fetch(`${API_URL}/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name, role })
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}

export async function login(email: string, password: string): Promise<{ token: string }> {
  const res = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}

export async function getMe(token: string): Promise<User> {
  const res = await fetch(`${API_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}

export async function updateProfile(token: string, profile: any): Promise<User> {
  const res = await fetch(`${API_URL}/profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(profile)
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}
