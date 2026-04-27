import { create } from "zustand";
import type { AuthResponse, User } from "../lib/types";
import { api, setAccessToken } from "../lib/api";

type AuthState = {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  status: "idle" | "loading";
  error?: string;
  bootstrap: () => void;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  refresh: () => Promise<boolean>;
  logout: () => Promise<void>;
};

const storageKey = "collab-code-auth";

function persist(auth: Pick<AuthState, "user" | "accessToken" | "refreshToken">) {
  localStorage.setItem(storageKey, JSON.stringify(auth));
}

function applySession(session: AuthResponse | Pick<AuthState, "user" | "accessToken" | "refreshToken">) {
  setAccessToken(session.accessToken);
  persist(session);
  return {
    user: session.user ?? null,
    accessToken: session.accessToken,
    refreshToken: session.refreshToken,
    isAuthenticated: Boolean(session.accessToken)
  };
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  status: "idle",
  bootstrap: () => {
    const raw = localStorage.getItem(storageKey);
    if (!raw) return;

    const session = JSON.parse(raw) as Pick<AuthState, "user" | "accessToken" | "refreshToken">;
    set(applySession(session));
  },
  login: async (email, password) => {
    set({ status: "loading", error: undefined });
    try {
      const { data } = await api.post<AuthResponse>("/auth/login", { email, password });
      set({ ...applySession(data), status: "idle" });
    } catch (error) {
      set({ status: "idle", error: error instanceof Error ? error.message : "Login failed" });
      throw error;
    }
  },
  register: async (name, email, password) => {
    set({ status: "loading", error: undefined });
    try {
      const { data } = await api.post<AuthResponse>("/auth/register", { name, email, password });
      set({ ...applySession(data), status: "idle" });
    } catch (error) {
      set({ status: "idle", error: error instanceof Error ? error.message : "Registration failed" });
      throw error;
    }
  },
  refresh: async () => {
    const refreshToken = get().refreshToken;
    const user = get().user;
    if (!refreshToken || !user) return false;

    const { data } = await api.post<Pick<AuthResponse, "accessToken" | "refreshToken">>("/auth/refresh", {
      refreshToken
    });
    const session = { user, accessToken: data.accessToken, refreshToken: data.refreshToken };
    set(applySession(session));
    return true;
  },
  logout: async () => {
    const refreshToken = get().refreshToken;
    try {
      if (refreshToken) await api.post("/auth/logout", { refreshToken });
    } finally {
      localStorage.removeItem(storageKey);
      setAccessToken(null);
      set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false });
    }
  }
}));
