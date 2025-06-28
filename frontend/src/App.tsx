import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginPage from 'pages/LoginPage';
import SignupPage from 'pages/SignupPage';
import MentorListPage from 'pages/MentorListPage';
import ProfilePage from 'pages/ProfilePage';
import MatchRequestPage from 'pages/MatchRequestPage';
import NotFound from 'components/NotFound';

const AppRoutes = () => {
  const location = useLocation();
  useEffect(() => {
    console.log('[MentorConnect] Frontend page entered:', location.pathname);
  }, [location.pathname]);
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/mentors" element={<MentorListPage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/match-requests" element={<MatchRequestPage />} />
      <Route path="/" element={<Navigate to="/mentors" />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

const App = () => (
  <BrowserRouter>
    <AppRoutes />
  </BrowserRouter>
);

export default App;
