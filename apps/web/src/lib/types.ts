export type User = {
  id: string;
  email: string;
  name: string;
};

export type DocumentSummary = {
  id: string;
  projectId: string;
  title: string;
  language: string;
  plainText: string;
  version: number;
  updatedAt: string;
};

export type DocumentRecord = DocumentSummary;

export type Project = {
  id: string;
  name: string;
  description?: string | null;
  documents: DocumentSummary[];
};

export type AuthResponse = {
  user: User;
  accessToken: string;
  refreshToken: string;
};

export type PresenceClient = {
  userId: string;
  name: string;
  color: string;
  cursor?: { lineNumber: number; column: number };
};
