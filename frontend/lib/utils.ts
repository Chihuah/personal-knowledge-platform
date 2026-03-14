export function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString("zh-TW", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
  } catch {
    return "—";
  }
}

export function formatDateTime(dateStr: string | null): string {
  if (!dateStr) return "—";
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString("zh-TW", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return "—";
  }
}

export function platformLabel(platform: string): string {
  const map: Record<string, string> = {
    facebook: "Facebook",
    threads: "Threads",
    youtube: "YouTube",
    twitter: "Twitter",
    blog: "Blog",
    podcast: "Podcast",
    generic_web: "Web",
  };
  return map[platform] ?? platform;
}

export function contentTypeLabel(type: string | null): string {
  if (!type) return "未知";
  const map: Record<string, string> = {
    article: "文章",
    post: "貼文",
    video: "影片",
    tool: "工具",
    tutorial: "教學",
    resource: "資源",
    news: "新聞",
    unknown: "未知",
  };
  return map[type] ?? type;
}

export function platformIcon(platform: string): string {
  const map: Record<string, string> = {
    facebook: "🌐",
    threads: "🧵",
    youtube: "▶️",
    twitter: "🐦",
    blog: "📝",
    podcast: "🎙️",
    generic_web: "🔗",
  };
  return map[platform] ?? "🔗";
}
