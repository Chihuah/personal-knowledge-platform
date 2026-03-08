import { Fira_Code, Fira_Sans } from "next/font/google";
import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

const firaSans = Fira_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-sans",
});

const firaCode = Fira_Code({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "Personal Knowledge Platform",
  description: "Capture, enrich, and retrieve personal knowledge.",
};

type RootLayoutProps = Readonly<{
  children: React.ReactNode;
}>;

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" className={`${firaSans.variable} ${firaCode.variable}`}>
      <body>
        <header className="site-header">
          <div className="site-header__inner">
            <Link className="brandmark" href="/">
              PKP
            </Link>
            <nav className="site-nav" aria-label="Primary">
              <Link href="/">Dashboard</Link>
              <Link href="/capture">Capture</Link>
              <Link href="/items">Library</Link>
            </nav>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}
