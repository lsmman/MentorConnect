import { User } from './user';

export type Mentor = User & {
  profile: {
    name: string;
    bio?: string;
    imageUrl: string;
    skills: string[];
  };
};
