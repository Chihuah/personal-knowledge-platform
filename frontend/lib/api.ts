export type KnowledgeItem = {
  id: string;
  source_url: string;
  source_platform: string;
  title: string | null;
  author: string | null;
  published_at: string | null;
  captured_at: string;
  thumbnail_url: string | null;
  description: string | null;
  short_summary: string | null;
  full_summary?: string | null;
  cleaned_content?: string | null;
  keywords: string[];
  category: string | null;
  content_type: string | null;
  processing_status: string;
  error_message: string | null;
  updated_at: string;
};

type Pagination = {
  total: number;
  page: number;
  page_size: number;
};

type DashboardBucket = {
  label: string;
  count: number;
};

type DashboardData = {
  total_count: number;
  recent_count: number;
  latest_items: KnowledgeItem[];
  failed_items: KnowledgeItem[];
  category_distribution: DashboardBucket[];
  status_distribution: DashboardBucket[];
};

type ListData = {
  items: KnowledgeItem[];
  pagination: Pagination;
};

const browserApiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
const serverApiBaseUrl =
  process.env.INTERNAL_API_BASE_URL ?? browserApiBaseUrl;

function getApiBaseUrl(): string {
  return typeof window === "undefined" ? serverApiBaseUrl : browserApiBaseUrl;
}

async function fetchApi<T>(path: string): Promise<T | null> {
  try {
    const response = await fetch(`${getApiBaseUrl()}${path}`, {
      cache: "no-store",
    });

    if (!response.ok) {
      return null;
    }

    const payload = (await response.json()) as { success: boolean; data: T };
    return payload.success ? payload.data : null;
  } catch {
    return null;
  }
}

export async function getDashboard(): Promise<DashboardData> {
  return (
    (await fetchApi<DashboardData>("/api/dashboard")) ?? {
      total_count: 0,
      recent_count: 0,
      latest_items: [],
      failed_items: [],
      category_distribution: [],
      status_distribution: [],
    }
  );
}

export async function getItems(params: {
  q?: string;
  status?: string;
  platform?: string;
}): Promise<ListData> {
  const query = new URLSearchParams();
  if (params.q) query.set("q", params.q);
  if (params.status) query.set("status", params.status);
  if (params.platform) query.set("platform", params.platform);

  return (
    (await fetchApi<ListData>(`/api/items?${query.toString()}`)) ?? {
      items: [],
      pagination: {
        total: 0,
        page: 1,
        page_size: 20,
      },
    }
  );
}

export async function getItem(id: string): Promise<KnowledgeItem | null> {
  return fetchApi<KnowledgeItem>(`/api/items/${id}`);
}
