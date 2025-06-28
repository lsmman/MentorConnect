import { MatchRequest } from '../types/matchRequest';

const API_URL = '/api';

export async function createMatchRequest(token: string, mentorId: number, menteeId: number, message: string) {
  const res = await fetch(`${API_URL}/match-requests`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ mentorId, menteeId, message })
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}

export async function getIncomingRequests(token: string): Promise<MatchRequest[]> {
  const res = await fetch(`${API_URL}/match-requests/incoming`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}

export async function getOutgoingRequests(token: string): Promise<MatchRequest[]> {
  const res = await fetch(`${API_URL}/match-requests/outgoing`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}

export async function acceptRequest(token: string, id: number) {
  const res = await fetch(`${API_URL}/match-requests/${id}/accept`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}

export async function rejectRequest(token: string, id: number) {
  const res = await fetch(`${API_URL}/match-requests/${id}/reject`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}

export async function cancelRequest(token: string, id: number) {
  const res = await fetch(`${API_URL}/match-requests/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}
