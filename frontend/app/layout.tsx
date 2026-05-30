import ThemeProvider from "@/components/ThemeProvider";
import { Toaster } from "sonner";
import "./globals.css";

export const metadata = {
  title: "Agent Trace Analyzer",
  description: "AI Agent Trace Analysis Dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
    >
      <body>
        <ThemeProvider>
          {children}
        </ThemeProvider>

        <Toaster richColors/>
      </body>
    </html>
  );
}