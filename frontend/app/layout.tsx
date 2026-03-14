import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "個人知識管理平台",
  description: "Personal Knowledge Platform - 管理與搜尋你的知識庫",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-TW" suppressHydrationWarning>
      <body className="bg-surface dark:bg-surface-dark text-gray-900 dark:text-gray-100 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
