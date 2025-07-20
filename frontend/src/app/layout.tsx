import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { CopilotKit } from "@copilotkit/react-core"; 
import "@copilotkit/react-ui/styles.css";


export default function RootLayout({ children }: {children: React.ReactNode}) {
  return (
    <html lang="en">
      <body>
        <CopilotKit 
          runtimeUrl="/api/copilotkit" 
          agent="agno_agent"
        >
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
