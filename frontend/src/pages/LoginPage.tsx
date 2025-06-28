import React, { useState } from 'react';
import AuthForm from '../components/AuthForm';
import { login } from '../api/auth';

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null);
  return (
    <div>
      <h2>로그인</h2>
      <AuthForm
        onSubmit={async (email, password) => {
          try {
            const { token } = await login(email, password);
            localStorage.setItem('token', token);
            window.location.href = '/mentors';
          } catch (e: any) {
            setError(e.message || '로그인 실패');
          }
        }}
      />
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
}
