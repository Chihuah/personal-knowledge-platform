import { EmptyState } from "../../components/empty-state";
import { ItemCard } from "../../components/item-card";
import { getItems } from "../../lib/api";


export const dynamic = "force-dynamic";

type ItemsPageProps = {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export default async function ItemsPage({ searchParams }: ItemsPageProps) {
  const params = await searchParams;
  const q = typeof params.q === "string" ? params.q : "";
  const status = typeof params.status === "string" ? params.status : "";
  const platform = typeof params.platform === "string" ? params.platform : "";

  const data = await getItems({
    q,
    status,
    platform,
  });

  return (
    <main className="shell">
      <section className="page-header">
        <p className="page-kicker">Library</p>
        <h1 className="page-title">Search your captured knowledge with context.</h1>
      </section>

      <section className="list-layout">
        <aside className="sidebar-panel">
          <p className="panel-label">Filters</p>
          <form action="/items" className="stack-list">
            <div className="form-field">
              <label htmlFor="q">Search</label>
              <input
                className="input"
                defaultValue={q}
                id="q"
                name="q"
                placeholder="AI agents, knowledge tools..."
              />
            </div>
            <div className="form-field">
              <label htmlFor="status">Status</label>
              <select className="select" defaultValue={status} id="status" name="status">
                <option value="">All statuses</option>
                <option value="queued">Queued</option>
                <option value="ready">Ready</option>
                <option value="failed">Failed</option>
              </select>
            </div>
            <div className="form-field">
              <label htmlFor="platform">Platform</label>
              <select
                className="select"
                defaultValue={platform}
                id="platform"
                name="platform"
              >
                <option value="">All platforms</option>
                <option value="generic_web">Generic Web</option>
                <option value="youtube">YouTube</option>
                <option value="facebook">Facebook</option>
                <option value="threads">Threads</option>
              </select>
            </div>
            <button className="button button-primary" type="submit">
              Apply filters
            </button>
          </form>
        </aside>

        <div className="panel">
          <div className="section-heading">
            <div>
              <p className="panel-label">Results</p>
              <h2>{data.pagination.total} items</h2>
            </div>
          </div>
          <div className="stack-list">
            {data.items.length > 0 ? (
              data.items.map((item) => <ItemCard item={item} key={item.id} />)
            ) : (
              <EmptyState
                title="No matching items"
                description="Try a broader query or capture a new URL."
                actionHref="/capture"
                actionLabel="Capture URL"
              />
            )}
          </div>
        </div>
      </section>
    </main>
  );
}
