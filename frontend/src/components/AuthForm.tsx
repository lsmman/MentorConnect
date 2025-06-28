import React, { useState } from 'react';
import { sanitizeInput } from '../utils/sanitize';

interface AuthFormProps {
  onSubmit: (
    email: string,
    password: string,
    name?: string,
    role?: 'mentor' | 'mentee',
  ) => void;
  isSignup?: boolean;
}

export default function AuthForm({ onSubmit, isSignup }: AuthFormProps) {
  const [form, setForm] = useState<{
    email: string;
    password: string;
    name: string;
    role: 'mentor' | 'mentee' | '';
  }>({ email: '', password: '', name: '', role: '' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: sanitizeInput(e.target.value) });
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(
          form.email,
          form.password,
          isSignup ? form.name : undefined,
          isSignup ? (form.role as 'mentor' | 'mentee' | undefined) : undefined,
        );
      }}
    >
      <input
        name="email"
        value={form.email}
        onChange={handleChange}
        placeholder="이메일"
        required
      />
      <input
        name="password"
        type="password"
        value={form.password}
        onChange={handleChange}
        placeholder="비밀번호"
        required
      />
      {isSignup && (
        <>
          <input
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="이름"
            required
          />
          <select
            name="role"
            value={form.role}
            onChange={(e) =>
              setForm({ ...form, role: e.target.value as 'mentor' | 'mentee' })
            }
            required
          >
            <option value="">역할 선택</option>
            <option value="mentor">멘토</option>
            <option value="mentee">멘티</option>
          </select>
        </>
      )}
      <button type="submit">{isSignup ? '회원가입' : '로그인'}</button>
    </form>
  );
}
