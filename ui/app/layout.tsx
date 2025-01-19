import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { CopilotKit } from "@copilotkit/react-core";

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Ace Attorney AI',
  description: 'An AI-powered legal debate system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <CopilotKit 
          runtimeUrl="/api/copilotkit"
          publicApiKey={process.env.NEXT_PUBLIC_COPILOTKIT_API_KEY || "default-public-key"}
        >
          {children}
        </CopilotKit>
      </body>
    </html>
  )
}