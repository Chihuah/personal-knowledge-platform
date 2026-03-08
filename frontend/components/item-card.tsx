import Link from "next/link";

import type { KnowledgeItem } from "../lib/api";
import { StatusPill } from "./status-pill";


type ItemCardProps = {
  item: KnowledgeItem;
};

export function ItemCard({ item }: ItemCardProps) {
  return (
    <Link className="item-card" href={`/items/${item.id}`}>
      <div className="item-card__top">
        <div>
          <h3>{item.title || item.source_url}</h3>
          <p className="muted-copy">{item.short_summary || "Awaiting summary."}</p>
        </div>
        <StatusPill status={item.processing_status} />
      </div>
      <div className="item-meta">
        <span>{item.source_platform}</span>
        <span>{item.category || "Uncategorized"}</span>
      </div>
      {item.keywords.length > 0 ? (
        <div className="tag-row">
          {item.keywords.slice(0, 4).map((keyword) => (
            <span className="tag" key={keyword}>
              {keyword}
            </span>
          ))}
        </div>
      ) : null}
    </Link>
  );
}
