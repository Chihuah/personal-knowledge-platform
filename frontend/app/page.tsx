import Link from "next/link";

import { EmptyState } from "../components/empty-state";
import { ItemCard } from "../components/item-card";
import { StatCard } from "../components/stat-card";
import { StatusPill } from "../components/status-pill";
import { getDashboard } from "../lib/api";


export const dynamic = "force-dynamic";

export default async function HomePage() {
  const dashboard = await getDashboard();

  return (
    <main className="shell">
      <section className="hero-grid">
        <div className="hero-copy">
          <p className="eyebrow">Personal Knowledge Platform</p>
          <h1>Capture once. Retrieve with context.</h1>
          <p className="lede">
            A private editorial workspace for URLs, parsed content, AI summaries,
            and searchable recall across your own knowledge archive.
          </p>
          <div className="hero-actions">
            <Link className="button button-primary" href="/capture">
              Add a URL
            </Link>
            <Link className="button button-secondary" href="/items">
              Browse library
            </Link>
          </div>
        </div>

        <aside className="hero-panel">
          <p className="panel-label">Pipeline snapshot</p>
          <div className="pipeline-stack">
            <div>
              <span>01</span>
              <strong>Queued ingestion</strong>
            </div>
            <div>
              <span>02</span>
              <strong>Parser routing</strong>
            </div>
            <div>
              <span>03</span>
              <strong>AI enrichment</strong>
            </div>
            <div>
              <span>04</span>
              <strong>Searchable archive</strong>
            </div>
          </div>
        </aside>
      </section>

      <section className="stats-grid" aria-label="Dashboard summary">
        <StatCard label="Total items" value={String(dashboard.total_count)} />
        <StatCard label="Last 7 days" value={String(dashboard.recent_count)} />
        <StatCard
          label="Failed items"
          value={String(dashboard.failed_items.length)}
        />
      </section>

      <section className="content-grid">
        <div className="panel">
          <div className="section-heading">
            <div>
              <p className="panel-label">Latest</p>
              <h2>Recent captures</h2>
            </div>
            <Link className="section-link" href="/items">
              View all
            </Link>
          </div>

          <div className="stack-list">
            {dashboard.latest_items.length > 0 ? (
              dashboard.latest_items.map((item) => (
                <ItemCard item={item} key={item.id} />
              ))
            ) : (
              <EmptyState
                title="No items yet"
                description="Start with a URL capture to build your library."
                actionHref="/capture"
                actionLabel="Capture first URL"
              />
            )}
          </div>
        </div>

        <div className="panel-stack">
          <section className="panel">
            <div className="section-heading">
              <div>
                <p className="panel-label">Status</p>
                <h2>Processing mix</h2>
              </div>
            </div>
            <div className="distribution-list">
              {dashboard.status_distribution.length > 0 ? (
                dashboard.status_distribution.map((entry) => (
                  <div className="distribution-row" key={entry.label}>
                    <StatusPill status={entry.label} />
                    <strong>{entry.count}</strong>
                  </div>
                ))
              ) : (
                <p className="muted-copy">No processing data yet.</p>
              )}
            </div>
          </section>

          <section className="panel">
            <div className="section-heading">
              <div>
                <p className="panel-label">Categories</p>
                <h2>Current spread</h2>
              </div>
            </div>
            <div className="distribution-list">
              {dashboard.category_distribution.length > 0 ? (
                dashboard.category_distribution.map((entry) => (
                  <div className="distribution-row" key={entry.label}>
                    <span className="distribution-label">{entry.label}</span>
                    <strong>{entry.count}</strong>
                  </div>
                ))
              ) : (
                <p className="muted-copy">Categories appear after enrichment.</p>
              )}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}
