import Link from "next/link";

import { EmptyState } from "../../../components/empty-state";
import { StatusPill } from "../../../components/status-pill";
import { getItem } from "../../../lib/api";


export const dynamic = "force-dynamic";

type ItemDetailPageProps = {
  params: Promise<{ id: string }>;
};

export default async function ItemDetailPage({ params }: ItemDetailPageProps) {
  const { id } = await params;
  const item = await getItem(id);

  if (!item) {
    return (
      <main className="shell">
        <section className="page-header">
          <p className="page-kicker">Item detail</p>
          <h1 className="page-title">This item is not available.</h1>
        </section>
        <EmptyState
          title="No detail data"
          description="The backend may be offline, or the item does not exist."
          actionHref="/items"
          actionLabel="Back to library"
        />
      </main>
    );
  }

  return (
    <main className="shell">
      <section className="page-header">
        <p className="page-kicker">Item detail</p>
        <h1 className="page-title">{item.title || "Untitled capture"}</h1>
        <div className="status-row">
          <StatusPill status={item.processing_status} />
          <Link className="button-like" href={item.source_url} target="_blank">
            Open source
          </Link>
        </div>
      </section>

      <section className="detail-grid">
        <div className="stack-list">
          <article className="detail-block">
            <div className="detail-header">
              <h2>Summary</h2>
            </div>
            <p className="detail-copy">
              {item.full_summary || item.short_summary || "Summary not available yet."}
            </p>
          </article>

          <article className="detail-block">
            <div className="detail-header">
              <h2>Captured content</h2>
            </div>
            <pre>{item.cleaned_content || "Content parsing has not completed yet."}</pre>
          </article>
        </div>

        <aside className="sidebar-panel">
          <p className="panel-label">Metadata</p>
          <div className="meta-grid">
            <div className="detail-block">
              <span className="mono-label">Platform</span>
              <p>{item.source_platform}</p>
            </div>
            <div className="detail-block">
              <span className="mono-label">Category</span>
              <p>{item.category || "Not assigned"}</p>
            </div>
            <div className="detail-block">
              <span className="mono-label">Keywords</span>
              <div className="tag-row">
                {item.keywords.length > 0 ? (
                  item.keywords.map((keyword) => (
                    <span className="tag" key={keyword}>
                      {keyword}
                    </span>
                  ))
                ) : (
                  <span className="muted-copy">No keywords yet.</span>
                )}
              </div>
            </div>
            <div className="detail-block">
              <span className="mono-label">Error</span>
              <p>{item.error_message || "None"}</p>
            </div>
          </div>
        </aside>
      </section>
    </main>
  );
}
