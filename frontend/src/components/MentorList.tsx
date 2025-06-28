import React from 'react';
import { Mentor } from '../types/mentor';

interface MentorListProps {
  mentors: Mentor[];
  onRequest?: (mentorId: number) => void;
}

const getProfileImage = (mentor: Mentor) => {
  if (mentor.profile?.imageUrl) return mentor.profile.imageUrl;
  return mentor.role === 'mentor'
    ? 'https://placehold.co/500x500.jpg?text=MENTOR'
    : 'https://placehold.co/500x500.jpg?text=MENTEE';
};

export default function MentorList({ mentors, onRequest }: MentorListProps) {
  if (!mentors.length) return <div>멘토가 없습니다.</div>;
  return (
    <ul className="mentor-list" data-testid="mentor-list">
      {mentors.map(m => (
        <li key={m.id} className="mentor-card" data-testid="mentor-card">
          <img
            src={getProfileImage(m)}
            alt="프로필"
            width={80}
            height={80}
            style={{ borderRadius: '50%' }}
          />
          <div>
            <b>{m.profile.name}</b> ({m.email})<br />
            <span>{m.profile.bio}</span><br />
            <span>기술: {m.profile.skills?.join(', ')}</span>
          </div>
          {onRequest && (
            <button className="mentor-request-btn" data-testid="mentor-request-btn" onClick={() => onRequest(m.id)}>매칭 요청</button>
          )}
        </li>
      ))}
    </ul>
  );
}
