"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { AuthGuard } from "../../components/auth-guard";
import { Navbar } from "../../components/navbar";
import { fetchItems, fetchCategories, KnowledgeItem, Pagination } from "../../lib/api";
import { formatDate, platformLabel, contentTypeLabel, platformIcon } from "../../lib/utils";

const PLATFORMS = [
  { value: "", label: "全部平台" },
  { value: "facebook", label: "Facebook" },
  { value: "threads", label: "Threads" },
  { value: "youtube", label: "YouTube" },
  { value: "twitter", label: "Twitter" },
  { value: "blog", label: "Blog" },
  { value: "podcast", label: "Podcast" },
  { value: "generic_web", label: "Web" },
];

const CONTENT_TYPES = [
  { value: "", label: "全部類型" },
  { value: "article", label: "文章" },
  { value: "post", label: "貼文" },
  { value: "video", label: "影片" },
  { value: "tool", label: "工具" },
  { value: "tutorial", label: "教學" },
  { value: "resource", label: "資源" },
  { value: "news", label: "新聞" },
];

const SORT_OPTIONS = [
  { value: "newest", label: "最新" },
  { value: "oldest", label: "最舊" },
  { value: "updated", label: "最近更新" },
];

function ItemCard({ item }: { item: KnowledgeItem }) {
  return (
    <Link
      href={`/items/${item.id}`}
      className="block bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-5 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-lg transition-all group"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <h3 className="text-base font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors line-clamp-2">
          {item.title || item.source_url}
        </h3>
        <span className="text-xs px-2.5 py-1 rounded-lg bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 whitespace-nowrap shrink-0 font-medium">
          {platformIcon(item.source_platform)} {platformLabel(item.source_platform)}
        </span>
      </div>

      <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 mb-3">
        {item.short_summary || "尚無摘要"}
      </p>

      <div className="flex items-center flex-wrap gap-2 mb-3">
        {item.keywords.slice(0, 4).map((kw) => (
          <span
            key={kw}
            className="text-xs px-2 py-0.5 rounded-md bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
          >
            {kw}
          </span>
        ))}
      </div>

      <div className="flex items-center gap-4 text-xs text-gray-400 dark:text-gray-500">
        {item.author && <span>{item.author}</span>}
        {item.category && <span className="capitalize">{item.category}</span>}
        <span>{contentTypeLabel(item.content_type)}</span>
        <span className="ml-auto">{formatDate(item.created_at)}</span>
      </div>
    </Link>
  );
}

function ItemsContent() {
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [pagination, setPagination] = useState<Pagination>({ page: 1, page_size: 20, total: 0 });
  const [categories, setCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [search, setSearch] = useState("");
  const [platform, setPlatform] = useState("");
  const [category, setCategory] = useState("");
  const [contentType, setContentType] = useState("");
  const [sort, setSort] = useState("newest");
  const [page, setPage] = useState(1);

  const loadItems = useCallback(async () => {
    setLoading(true);
    try {
      const result = await fetchItems({
        q: search || undefined,
        platform: platform || undefined,
        category: category || undefined,
        content_type: contentType || undefined,
        sort,
        page,
        page_size: 20,
      });
      setItems(result.items);
      setPagination(result.pagination);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [search, platform, category, contentType, sort, page]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  useEffect(() => {
    fetchCategories().then(setCategories).catch(console.error);
  }, []);

  const totalPages = Math.ceil(pagination.total / pagination.page_size) || 1;

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setPage(1);
    loadItems();
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">知識庫</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">瀏覽與搜尋所有知識條目</p>
      </div>

      {/* Search & Filters */}
      <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-4 mb-6">
        <form onSubmit={handleSearch} className="flex gap-3 mb-4">
          <div className="flex-1 relative">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="搜尋標題、摘要、關鍵字..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-border-light dark:border-border-dark bg-surface dark:bg-surface-dark text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium transition-colors shrink-0"
          >
            搜尋
          </button>
        </form>

        <div className="flex flex-wrap gap-3">
          <select
            value={platform}
            onChange={(e) => { setPlatform(e.target.value); setPage(1); }}
            className="px-3 py-2 rounded-lg border border-border-light dark:border-border-dark bg-surface dark:bg-surface-dark text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {PLATFORMS.map((p) => (
              <option key={p.value} value={p.value}>{p.label}</option>
            ))}
          </select>

          <select
            value={category}
            onChange={(e) => { setCategory(e.target.value); setPage(1); }}
            className="px-3 py-2 rounded-lg border border-border-light dark:border-border-dark bg-surface dark:bg-surface-dark text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">全部分類</option>
            {categories.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>

          <select
            value={contentType}
            onChange={(e) => { setContentType(e.target.value); setPage(1); }}
            className="px-3 py-2 rounded-lg border border-border-light dark:border-border-dark bg-surface dark:bg-surface-dark text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {CONTENT_TYPES.map((ct) => (
              <option key={ct.value} value={ct.value}>{ct.label}</option>
            ))}
          </select>

          <select
            value={sort}
            onChange={(e) => { setSort(e.target.value); setPage(1); }}
            className="px-3 py-2 rounded-lg border border-border-light dark:border-border-dark bg-surface dark:bg-surface-dark text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {SORT_OPTIONS.map((s) => (
              <option key={s.value} value={s.value}>{s.label}</option>
            ))}
          </select>

          {(search || platform || category || contentType) && (
            <button
              onClick={() => { setSearch(""); setPlatform(""); setCategory(""); setContentType(""); setPage(1); }}
              className="px-3 py-2 rounded-lg text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              清除篩選
            </button>
          )}
        </div>
      </div>

      {/* Results info */}
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          共 <span className="font-medium text-gray-900 dark:text-white">{pagination.total}</span> 筆結果
        </p>
      </div>

      {/* Items list */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-pulse text-primary-600 dark:text-primary-400">載入中...</div>
        </div>
      ) : items.length === 0 ? (
        <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-12 text-center">
          <svg className="w-12 h-12 mx-auto text-gray-300 dark:text-gray-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <p className="text-gray-500 dark:text-gray-400 mb-2">找不到符合條件的知識條目</p>
          <p className="text-sm text-gray-400 dark:text-gray-500">嘗試調整搜尋條件或篩選器</p>
        </div>
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <ItemCard key={item.id} item={item} />
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 mt-8">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page <= 1}
            className="px-3 py-2 rounded-lg border border-border-light dark:border-border-dark text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            上一頁
          </button>
          <span className="text-sm text-gray-500 dark:text-gray-400 px-3">
            第 {page} / {totalPages} 頁
          </span>
          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page >= totalPages}
            className="px-3 py-2 rounded-lg border border-border-light dark:border-border-dark text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            下一頁
          </button>
        </div>
      )}
    </div>
  );
}

export default function ItemsPage() {
  return (
    <AuthGuard>
      <Navbar />
      <ItemsContent />
    </AuthGuard>
  );
}
