"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken, clearAuth } from "../lib/auth";
import { verifyToken } from "../lib/api";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [checking, setChecking] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.replace("/login");
      return;
    }
    verifyToken(token)
      .then((res) => {
        if (res.valid) {
          setAuthenticated(true);
        } else {
          clearAuth();
          router.replace("/login");
        }
      })
      .catch(() => {
        clearAuth();
        router.replace("/login");
      })
      .finally(() => setChecking(false));
  }, [router]);

  if (checking) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-surface dark:bg-surface-dark">
        <div className="animate-pulse text-primary-600 dark:text-primary-400 text-lg">載入中...</div>
      </div>
    );
  }

  if (!authenticated) return null;

  return <>{children}</>;
}
