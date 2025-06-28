import { Mentor } from '../types/mentor';

const API_URL = '/api';

export async function getMentors(token: string, skill?: string, orderBy?: string): Promise<Mentor[]> {
  const params = new URLSearchParams();
  if (skill) params.append('skill', skill);
  if (orderBy) params.append('order_by', orderBy);
  const res = await fetch(`${API_URL}/mentors?${params.toString()}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}
