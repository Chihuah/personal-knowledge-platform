"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";


const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export function CaptureForm() {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [feedback, setFeedback] = useState<{ kind: "error" | "success"; message: string } | null>(null);
  const [isPending, startTransition] = useTransition();

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFeedback(null);

    try {
      const response = await fetch(`${apiBaseUrl}/api/items`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const payload = await response.json();
      if (!response.ok || !payload.success) {
        throw new Error(payload.error?.message || "Capture failed.");
      }

      setFeedback({
        kind: "success",
        message: "URL captured and queued for processing.",
      });
      setUrl("");
      startTransition(() => {
        router.push(`/items/${payload.data.id}`);
        router.refresh();
      });
    } catch (error) {
      setFeedback({
        kind: "error",
        message: error instanceof Error ? error.message : "Capture failed.",
      });
    }
  }

  return (
    <form className="capture-form stack-list" onSubmit={handleSubmit}>
      <div className="form-field">
        <label htmlFor="url">Source URL</label>
        <input
          className="input"
          id="url"
          name="url"
          onChange={(event) => setUrl(event.target.value)}
          placeholder="https://example.com/article"
          required
          type="url"
          value={url}
        />
      </div>

      <div className="button-row">
        <button className="button button-primary" disabled={isPending} type="submit">
          {isPending ? "Capturing..." : "Capture URL"}
        </button>
      </div>

      {feedback ? (
        <div className={`feedback ${feedback.kind === "error" ? "feedback-error" : "feedback-success"}`}>
          {feedback.message}
        </div>
      ) : null}
    </form>
  );
}
