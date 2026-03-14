const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export interface KnowledgeItem {
  id: string;
  source_url: string;
  source_platform: string;
  title: string | null;
  author: string | null;
  published_at: string | null;
  short_summary: string | null;
  keywords: string[];
  category: string | null;
  content_type: string | null;
  processing_status: string;
  updated_at: string;
  created_at: string;
}

export interface KnowledgeItemDetail extends KnowledgeItem {
  raw_content: string | null;
  full_summary: string | null;
}

export interface Pagination {
  page: number;
  page_size: number;
  total: number;
}

export interface DashboardBucket {
  label: string;
  count: number;
}

export interface DashboardData {
  total_count: number;
  recent_count: number;
  latest_items: KnowledgeItem[];
  category_distribution: DashboardBucket[];
  platform_distribution: DashboardBucket[];
  content_type_distribution: DashboardBucket[];
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: { code: string; message: string };
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  const json: ApiResponse<T> = await res.json();
  if (!res.ok || !json.success) {
    throw new Error(json.error?.message ?? "API request failed");
  }
  return json.data;
}

export async function login(username: string, password: string): Promise<{ token: string; username: string }> {
  return apiFetch("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export async function verifyToken(token: string): Promise<{ valid: boolean; username: string }> {
  return apiFetch(`/api/auth/verify?token=${encodeURIComponent(token)}`);
}

export async function fetchDashboard(): Promise<DashboardData> {
  return apiFetch("/api/dashboard");
}

export interface ItemListParams {
  q?: string;
  platform?: string;
  category?: string;
  content_type?: string;
  page?: number;
  page_size?: number;
  sort?: string;
}

export async function fetchItems(params: ItemListParams = {}): Promise<{ items: KnowledgeItem[]; pagination: Pagination }> {
  const searchParams = new URLSearchParams();
  if (params.q) searchParams.set("q", params.q);
  if (params.platform) searchParams.set("platform", params.platform);
  if (params.category) searchParams.set("category", params.category);
  if (params.content_type) searchParams.set("content_type", params.content_type);
  if (params.page) searchParams.set("page", String(params.page));
  if (params.page_size) searchParams.set("page_size", String(params.page_size));
  if (params.sort) searchParams.set("sort", params.sort);
  const qs = searchParams.toString();
  return apiFetch(`/api/items${qs ? `?${qs}` : ""}`);
}

export async function fetchItem(id: string): Promise<KnowledgeItemDetail> {
  return apiFetch(`/api/items/${id}`);
}

export async function fetchCategories(): Promise<string[]> {
  return apiFetch("/api/items/categories");
}
