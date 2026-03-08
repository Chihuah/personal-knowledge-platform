import { CaptureForm } from "../../components/capture-form";


export default function CapturePage() {
  return (
    <main className="shell">
      <section className="page-header">
        <p className="page-kicker">Capture</p>
        <h1 className="page-title">Turn loose links into structured knowledge.</h1>
        <p className="lede">
          Submit a URL, queue parsing, and let the backend enrich it into a
          searchable knowledge item.
        </p>
      </section>

      <section className="capture-grid">
        <CaptureForm />
        <aside className="sidebar-panel">
          <p className="panel-label">What happens next</p>
          <div className="pipeline-stack">
            <div>
              <span>01</span>
              <strong>URL validation and deduplication</strong>
            </div>
            <div>
              <span>02</span>
              <strong>Source-aware parsing</strong>
            </div>
            <div>
              <span>03</span>
              <strong>AI summary and tagging</strong>
            </div>
            <div>
              <span>04</span>
              <strong>Search and dashboard availability</strong>
            </div>
          </div>
        </aside>
      </section>
    </main>
  );
}
