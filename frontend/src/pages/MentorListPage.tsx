import React, { useEffect, useState } from 'react';
import { getMentors } from '../api/mentors';
import MentorList from '../components/MentorList';
import { Mentor } from '../types/mentor';
import { requestMatch } from '../api/requestMatch';

export default function MentorListPage() {
  const [mentors, setMentors] = useState<Mentor[]>([]);
  const [skill, setSkill] = useState('');
  const [orderBy, setOrderBy] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token') || '';
    getMentors(token, skill, orderBy)
      .then(setMentors)
      .catch(e => setError(e.message || '멘토 조회 실패'));
  }, [skill, orderBy]);

  return (
    <div>
      <h2>멘토 목록</h2>
      <input
        placeholder="기술로 필터"
        value={skill}
        onChange={e => setSkill(e.target.value)}
      />
      <select value={orderBy} onChange={e => setOrderBy(e.target.value)}>
        <option value="">정렬 없음</option>
        <option value="name">이름순</option>
        <option value="skill">기술순</option>
      </select>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {toast && <div className="toast-success" data-testid="toast-success">{toast}</div>}
      <MentorList
        mentors={mentors}
        onRequest={async (mentorId) => {
          try {
            const token = localStorage.getItem('token') || '';
            await requestMatch(token, mentorId, '멘토링 받고 싶어요!');
            setToast('요청 완료');
            setTimeout(() => setToast(null), 2000);
          } catch (e: any) {
            setToast('요청 실패: ' + (e.message || '')); 
            setTimeout(() => setToast(null), 2000);
          }
        }}
      />
    </div>
  );
}
