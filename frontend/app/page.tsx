"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AuthGuard } from "../components/auth-guard";
import { Navbar } from "../components/navbar";
import { fetchDashboard, DashboardData, KnowledgeItem } from "../lib/api";
import { formatDate, platformLabel, contentTypeLabel } from "../lib/utils";

function StatCard({ label, value, icon }: { label: string; value: string | number; icon: React.ReactNode }) {
  return (
    <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-5 flex items-start gap-4">
      <div className="w-11 h-11 rounded-lg bg-primary-100 dark:bg-primary-900/40 flex items-center justify-center text-primary-600 dark:text-primary-400 shrink-0">
        {icon}
      </div>
      <div>
        <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
        <p className="text-2xl font-bold text-gray-900 dark:text-white mt-0.5">{value}</p>
      </div>
    </div>
  );
}

function DistributionCard({ title, data }: { title: string; data: { label: string; count: number }[] }) {
  const total = data.reduce((sum, d) => sum + d.count, 0) || 1;
  const colors = [
    "bg-primary-500", "bg-indigo-500", "bg-violet-500", "bg-blue-500",
    "bg-cyan-500", "bg-teal-500", "bg-emerald-500", "bg-amber-500",
  ];
  return (
    <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-5">
      <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">{title}</h3>
      {data.length === 0 ? (
        <p className="text-sm text-gray-400 dark:text-gray-500">尚無資料</p>
      ) : (
        <div className="space-y-3">
          {data.slice(0, 6).map((item, i) => (
            <div key={item.label}>
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="text-gray-600 dark:text-gray-400 capitalize">{item.label}</span>
                <span className="font-medium text-gray-900 dark:text-white">{item.count}</span>
              </div>
              <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${colors[i % colors.length]} transition-all duration-500`}
                  style={{ width: `${Math.max((item.count / total) * 100, 2)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function LatestItemCard({ item }: { item: KnowledgeItem }) {
  return (
    <Link
      href={`/items/${item.id}`}
      className="block bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-4 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-md transition-all group"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <h4 className="text-sm font-semibold text-gray-900 dark:text-white truncate group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
            {item.title || item.source_url}
          </h4>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
            {item.short_summary || "尚無摘要"}
          </p>
        </div>
        <span className="text-xs px-2 py-1 rounded-md bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 whitespace-nowrap shrink-0">
          {platformLabel(item.source_platform)}
        </span>
      </div>
      <div className="flex items-center gap-3 mt-3 text-xs text-gray-400 dark:text-gray-500">
        {item.category && <span className="capitalize">{item.category}</span>}
        <span>{formatDate(item.created_at)}</span>
      </div>
    </Link>
  );
}

function DashboardContent() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-pulse text-primary-600 dark:text-primary-400">載入中...</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-20 text-gray-500 dark:text-gray-400">
        無法載入儀表板資料
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">儀表板</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">知識庫總覽與統計</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <StatCard
          label="知識條目總數"
          value={data.total_count}
          icon={
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          }
        />
        <StatCard
          label="近 7 天新增"
          value={data.recent_count}
          icon={
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
        />
        <StatCard
          label="分類數量"
          value={data.category_distribution.length}
          icon={
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
          }
        />
      </div>

      {/* Charts + Latest */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Distributions */}
        <div className="lg:col-span-1 space-y-6">
          <DistributionCard title="分類分佈" data={data.category_distribution} />
          <DistributionCard title="來源平台" data={data.platform_distribution} />
          <DistributionCard title="內容類型" data={data.content_type_distribution} />
        </div>

        {/* Latest items */}
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">最近新增</h2>
            <Link
              href="/items"
              className="text-sm text-primary-600 dark:text-primary-400 hover:underline"
            >
              查看全部 →
            </Link>
          </div>
          {data.latest_items.length === 0 ? (
            <div className="bg-card dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-8 text-center">
              <p className="text-gray-500 dark:text-gray-400 mb-4">知識庫尚無條目</p>
              <p className="text-sm text-gray-400 dark:text-gray-500">
                透過 API 提交知識條目後，將會顯示在這裡
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {data.latest_items.map((item) => (
                <LatestItemCard key={item.id} item={item} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <AuthGuard>
      <Navbar />
      <DashboardContent />
    </AuthGuard>
  );
}
