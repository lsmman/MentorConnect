export type UserRole = 'mentor' | 'mentee';

export interface UserProfile {
  name: string;
  bio?: string;
  imageUrl: string;
  skills?: string[];
}

export interface User {
  id: number;
  email: string;
  role: UserRole;
  profile: UserProfile;
}
