import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/shared/theme-provider";
import { ReactQueryProvider } from "@/components/shared/react-query-provider";
import { LanguageProvider } from "@/components/shared/language-provider";
import { ErrorBoundary } from "@/components/shared/error-boundary";
import { Toaster } from "sonner";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Multi-Agent Research System",
  description: "AI-powered research system with collaborative agents analyzing complex topics in real-time",
  keywords: ["AI", "research", "multi-agent", "LLM", "automation"],
  authors: [{ name: "Your Name" }],
  openGraph: {
    title: "Multi-Agent Research System",
    description: "Watch AI agents collaborate to conduct comprehensive research",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <ErrorBoundary>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            <LanguageProvider>
              <ReactQueryProvider>
                {children}
                <Toaster richColors position="top-right" />
              </ReactQueryProvider>
            </LanguageProvider>
          </ThemeProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}

