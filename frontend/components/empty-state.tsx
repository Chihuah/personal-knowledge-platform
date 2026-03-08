import Link from "next/link";


type EmptyStateProps = {
  title: string;
  description: string;
  actionHref: string;
  actionLabel: string;
};

export function EmptyState({
  title,
  description,
  actionHref,
  actionLabel,
}: EmptyStateProps) {
  return (
    <div className="empty-state">
      <h2>{title}</h2>
      <p>{description}</p>
      <Link className="button button-secondary" href={actionHref}>
        {actionLabel}
      </Link>
    </div>
  );
}
