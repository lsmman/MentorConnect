import React, { useState } from 'react';
import { sanitizeInput } from '../utils/sanitize';

interface AuthFormProps {
  onSubmit: (email: string, password: string, name?: string, role?: 'mentor' | 'mentee') => void;
  isSignup?: boolean;
}

export default function AuthForm({ onSubmit, isSignup }: AuthFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState<'mentor' | 'mentee'>('mentee');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: sanitizeInput(e.target.value) });
  };

  return (
    <form
      onSubmit={e => {
        e.preventDefault();
        onSubmit(email, password, isSignup ? name : undefined, isSignup ? role : undefined);
      }}
    >
      <input
        type="email"
        name="email"
        data-testid="email-input"
        placeholder="이메일"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        name="password"
        data-testid="password-input"
        placeholder="비밀번호"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
      />
      {isSignup && (
        <>
          <input
            type="text"
            name="name"
            data-testid="name-input"
            placeholder="이름"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
          <select
            name="role"
            data-testid="role-select"
            value={role}
            onChange={e => setRole(e.target.value as 'mentor' | 'mentee')}
          >
            <option value="mentor">멘토</option>
            <option value="mentee">멘티</option>
          </select>
        </>
      )}
      <button type="submit">{isSignup ? '회원가입' : '로그인'}</button>
    </form>
  );
}
