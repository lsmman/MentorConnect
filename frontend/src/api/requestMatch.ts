import { getMe } from './auth';

const API_URL = '/api';

export async function requestMatch(token: string, mentorId: number, message: string) {
  // menteeId는 토큰에서 조회
  const me = await getMe(token);
  if (!me || me.role !== 'mentee') throw new Error('멘티만 요청 가능');
  const res = await fetch(`${API_URL}/match-requests`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ mentorId, menteeId: me.id, message })
  });
  if (!res.ok) throw await res.json();
  return await res.json();
}
