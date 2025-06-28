import React, { useEffect, useState } from 'react';
import { getMe, updateProfile } from '../api/auth';
import { User } from '../types/user';
import { sanitizeInput } from '../utils/sanitize';

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);
  const [bio, setBio] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [skills, setSkills] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token') || '';
    getMe(token)
      .then(u => {
        setUser(u);
        setBio(u.profile.bio || '');
        setSkills(u.profile.skills?.join(',') || '');
      })
      .catch(e => setError(e.message || '내 정보 조회 실패'));
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setBio(sanitizeInput(e.target.value));
  };

  const handleUpdate = async () => {
    try {
      const token = localStorage.getItem('token') || '';
      let imageBase64 = undefined;
      if (image) {
        const reader = new FileReader();
        reader.onload = async () => {
          imageBase64 = (reader.result as string).split(',')[1];
          await updateProfile(token, {
            id: user!.id,
            name: user!.profile.name,
            role: user!.role,
            bio,
            image: imageBase64,
            skills: user!.role === 'mentor' ? skills.split(',').map(s => s.trim()) : undefined
          });
          window.location.reload();
        };
        reader.readAsDataURL(image);
      } else {
        await updateProfile(token, {
          id: user!.id,
          name: user!.profile.name,
          role: user!.role,
          bio,
          skills: user!.role === 'mentor' ? skills.split(',').map(s => s.trim()) : undefined
        });
        window.location.reload();
      }
    } catch (e: any) {
      handleError(e);
    }
  };

  const handleError = (err: any) => {
    if (err.response && err.response.data && err.response.data.code) {
      setError(`${err.response.data.message}: ${err.response.data.detail}`);
    } else {
      setError('알 수 없는 에러');
    }
  };

  if (!user) return <div>로딩중...</div>;
  return (
    <div>
      <h2>내 프로필</h2>
      <div>
        <b>{user.profile.name}</b> ({user.email})<br />
        <img
          src={user.profile.imageUrl || (user.role === 'mentor'
            ? 'https://placehold.co/500x500.jpg?text=MENTOR'
            : 'https://placehold.co/500x500.jpg?text=MENTEE')}
          alt="프로필"
          width={100}
          height={100}
          style={{ borderRadius: '50%' }}
        />
      </div>
      <div>
        <textarea value={bio} onChange={handleChange} placeholder="소개" />
      </div>
      {user.role === 'mentor' && (
        <div>
          <input
            value={skills}
            onChange={e => setSkills(e.target.value)}
            placeholder="기술(쉼표로 구분)"
          />
        </div>
      )}
      <div>
        <input type="file" accept=".jpg,.png" onChange={e => setImage(e.target.files?.[0] || null)} />
      </div>
      <button onClick={handleUpdate}>수정</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
}
