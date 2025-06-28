import React, { useEffect, useState } from 'react';
import { getIncomingRequests, getOutgoingRequests, acceptRequest, rejectRequest, cancelRequest } from '../api/matchRequests';
import { MatchRequest } from '../types/matchRequest';

const MatchRequestPage: React.FC = () => {
  const [incoming, setIncoming] = useState<MatchRequest[]>([]);
  const [outgoing, setOutgoing] = useState<MatchRequest[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getIncomingRequests()
      .then(setIncoming)
      .catch(() => setIncoming([]));
    getOutgoingRequests()
      .then(setOutgoing)
      .catch(() => setOutgoing([]));
  }, []);

  const handleAccept = async (id: number) => {
    try {
      await acceptRequest(id);
      setIncoming((prev) => prev.map((r) => (r.id === id ? { ...r, status: 'accepted' } : r)));
    } catch (e) {
      setError('수락 실패');
    }
  };
  const handleReject = async (id: number) => {
    try {
      await rejectRequest(id);
      setIncoming((prev) => prev.map((r) => (r.id === id ? { ...r, status: 'rejected' } : r)));
    } catch (e) {
      setError('거절 실패');
    }
  };
  const handleCancel = async (id: number) => {
    try {
      await cancelRequest(id);
      setOutgoing((prev) => prev.map((r) => (r.id === id ? { ...r, status: 'cancelled' } : r)));
    } catch (e) {
      setError('취소 실패');
    }
  };

  return (
    <div>
      <h2>받은 요청 (멘토)</h2>
      <ul>
        {incoming.map((req) => (
          <li key={req.id}>
            {req.message} - {req.status}
            {req.status === 'pending' && (
              <>
                <button onClick={() => handleAccept(req.id)}>수락</button>
                <button onClick={() => handleReject(req.id)}>거절</button>
              </>
            )}
          </li>
        ))}
      </ul>
      <h2>보낸 요청 (멘티)</h2>
      <ul>
        {outgoing.map((req) => (
          <li key={req.id}>
            {req.status}
            {req.status === 'pending' && <button onClick={() => handleCancel(req.id)}>취소</button>}
          </li>
        ))}
      </ul>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
};

export default MatchRequestPage;
