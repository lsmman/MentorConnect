import React, { useState } from 'react';
import AuthForm from '../components/AuthForm';
import { signup } from '../api/auth';

export default function SignupPage() {
  const [error, setError] = useState<string | null>(null);
  return (
    <div>
      <h2>회원가입</h2>
      <AuthForm
        isSignup
        onSubmit={async (email, password, name, role) => {
          try {
            await signup(email, password, name!, role!);
            window.location.href = '/login';
          } catch (e: any) {
            setError(e.message || '회원가입 실패');
          }
        }}
      />
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
}
