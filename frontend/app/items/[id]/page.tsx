"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { AuthGuard } from "../../../components/auth-guard";
import { Navbar } from "../../../components/navbar";
import { fetchItem, KnowledgeItemDetail } from "../../../lib/api";
import { formatDateTime, platformLabel, contentTypeLabel, platformIcon } from "../../../lib/utils";

function DetailContent() {
  const params = useParams();
  const router = useRouter();
  const [item, setItem] = useState<KnowledgeItemDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const id = params.id as string;
    if (!id) return;
    fetchItem(id)
      .then(setItem)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-pulse text-primary-600 dark:text-primary-400">載入中...</div>
      </div>
    );
  }

  if (error || !item) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6 text-center">
          <p className="text-red-700 dark:text-red-400">{error || "找不到此條目"}</p>
          <Link href="/items" className="text-sm text-primary-600 dark:text-primary-400 hover:underline mt-2 inline-block">
            返回知識庫
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      {/* Back link */}
      <Link
        href="/items"
        className="inline-flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors mb-6"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path d="M15 19l-7-7 7-7" />
        </svg>
        返回知識庫
      </Link>

      {/* Header */}
      <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-6 mb-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white leading-relaxed">
            {item.title || "無標題"}
          </h1>
          <span className="text-xs px-2.5 py-1 rounded-lg bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 whitespace-nowrap shrink-0 font-medium">
            {platformIcon(item.source_platform)} {platformLabel(item.source_platform)}
          </span>
        </div>

        {/* Meta grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-gray-400 dark:text-gray-500 text-xs mb-0.5">發文者</p>
            <p className="text-gray-700 dark:text-gray-300">{item.author || "—"}</p>
          </div>
          <div>
            <p className="text-gray-400 dark:text-gray-500 text-xs mb-0.5">發文時間</p>
            <p className="text-gray-700 dark:text-gray-300">{formatDateTime(item.published_at)}</p>
          </div>
          <div>
            <p className="text-gray-400 dark:text-gray-500 text-xs mb-0.5">內容類型</p>
            <p className="text-gray-700 dark:text-gray-300">{contentTypeLabel(item.content_type)}</p>
          </div>
          <div>
            <p className="text-gray-400 dark:text-gray-500 text-xs mb-0.5">分類</p>
            <p className="text-gray-700 dark:text-gray-300 capitalize">{item.category || "未分類"}</p>
          </div>
        </div>

        {/* Source URL */}
        <div className="mt-4 pt-4 border-t border-border-light dark:border-border-dark">
          <p className="text-gray-400 dark:text-gray-500 text-xs mb-1">原始連結</p>
          <a
            href={item.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary-600 dark:text-primary-400 hover:underline break-all"
          >
            {item.source_url}
          </a>
        </div>

        {/* Keywords */}
        {item.keywords.length > 0 && (
          <div className="mt-4 pt-4 border-t border-border-light dark:border-border-dark">
            <p className="text-gray-400 dark:text-gray-500 text-xs mb-2">關鍵字</p>
            <div className="flex flex-wrap gap-2">
              {item.keywords.map((kw) => (
                <span
                  key={kw}
                  className="text-xs px-2.5 py-1 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
                >
                  {kw}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Timestamps */}
        <div className="mt-4 pt-4 border-t border-border-light dark:border-border-dark flex flex-wrap gap-6 text-xs text-gray-400 dark:text-gray-500">
          <span>建立時間：{formatDateTime(item.created_at)}</span>
          <span>更新時間：{formatDateTime(item.updated_at)}</span>
        </div>
      </div>

      {/* Short Summary */}
      {item.short_summary && (
        <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-6 mb-6">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            短摘要
          </h2>
          <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{item.short_summary}</p>
        </div>
      )}

      {/* Full Summary */}
      {item.full_summary && (
        <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-6 mb-6">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            長摘要
          </h2>
          <div className="text-gray-600 dark:text-gray-400 leading-relaxed whitespace-pre-wrap">{item.full_summary}</div>
        </div>
      )}

      {/* Raw Content */}
      {item.raw_content && (
        <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-6">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
            <svg className="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            完整原文
          </h2>
          <div className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed whitespace-pre-wrap max-h-96 overflow-y-auto rounded-lg bg-gray-50 dark:bg-gray-900 p-4 border border-border-light dark:border-border-dark">
            {item.raw_content}
          </div>
        </div>
      )}
    </div>
  );
}

export default function ItemDetailPage() {
  return (
    <AuthGuard>
      <Navbar />
      <DetailContent />
    </AuthGuard>
  );
}
