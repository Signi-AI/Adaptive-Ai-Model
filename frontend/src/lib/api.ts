/*
 * Development has no fixed IP address: opening Vite at 127.0.0.1, localhost,
 * or the school-server LAN address must call the backend on that same host.
 * A production build supplies VITE_API_BASE_URL from .env.production (or the
 * hosting provider's build environment) and therefore calls the deployed API.
 */
const localApiUrl = () => {
  if (typeof window === "undefined") return "http://127.0.0.1:8000";
  return `http://${window.location.hostname}:8000`;
};

const baseUrl = (import.meta.env.VITE_API_BASE_URL?.trim() || localApiUrl()).replace(/\/$/, "");

type Tokens = { access_token: string; refresh_token: string; expires_at: string };

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) { super(message); this.status = status; }
}

const tokenKey = "toalm_tokens";
const activeUsernameKey = "toalm_active_username";
const studentCacheKeys = [
  "student_profile_data",
  "student_profile_image",
  "learn_recent",
  "learn_chat_sessions",
  "selectedRecentLesson",
];
export const getTokens = (): Tokens | null => {
  try { return JSON.parse(localStorage.getItem(tokenKey) || "null") as Tokens | null; }
  catch { localStorage.removeItem(tokenKey); return null; }
};
export const clearTokens = () => localStorage.removeItem(tokenKey);
const saveTokens = (tokens: Tokens) => localStorage.setItem(tokenKey, JSON.stringify(tokens));

async function message(response: Response) {
  try { const body = await response.json(); if (typeof body.detail === "string") return body.detail; }
  catch { /* use a safe fallback below */ }
  return "The request could not be completed. Please try again.";
}

async function refresh(): Promise<boolean> {
  const tokens = getTokens();
  if (!tokens) return false;
  try {
    const response = await fetch(`${baseUrl}/auth/refresh`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ refresh_token: tokens.refresh_token }) });
    if (!response.ok) { clearTokens(); return false; }
    saveTokens(await response.json() as Tokens);
    return true;
  } catch { return false; }
}

export async function api<T>(path: string, init: RequestInit = {}, allowRefresh = true): Promise<T> {
  const headers = new Headers(init.headers);
  const tokens = getTokens();
  if (tokens) headers.set("Authorization", `Bearer ${tokens.access_token}`);
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  let response: Response;
  try { response = await fetch(`${baseUrl}${path}`, { ...init, headers }); }
  catch { throw new ApiError(0, "Cannot reach the learning server. Check that the backend is running."); }
  if (response.status === 401 && allowRefresh && await refresh()) return api<T>(path, init, false);
  if (!response.ok) throw new ApiError(response.status, await message(response));
  return response.status === 204 ? undefined as T : response.json() as Promise<T>;
}

export async function signIn(username: string, password: string) {
  const response = await fetch(`${baseUrl}/auth/login`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams({ username, password, device_label: "TOALM web" }) });
  if (!response.ok) throw new ApiError(response.status, await message(response));
  const account = username.trim().toLocaleLowerCase();
  // Browser-only details (photo, chat display history and profile cache) must
  // never be shown to the next student using this shared computer.
  if (localStorage.getItem(activeUsernameKey) !== account) {
    studentCacheKeys.forEach((key) => localStorage.removeItem(key));
  }
  localStorage.setItem(activeUsernameKey, account);
  saveTokens(await response.json() as Tokens);
}

export async function registerStudent(input: { username: string; full_name: string; password: string; class_level: string }) {
  await api("/auth/register", { method: "POST", body: JSON.stringify(input) });
}
