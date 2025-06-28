export type MatchStatus = 'pending' | 'accepted' | 'rejected' | 'cancelled';

export interface MatchRequest {
  id: number;
  mentorId: number;
  menteeId: number;
  message?: string;
  status: MatchStatus;
}
