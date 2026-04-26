import type { Metadata, Viewport } from 'next';
import { ClientWarmUp } from '@/components/ClientWarmUp';
import { AuthProvider } from '@/context/AuthContext';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: 'Nova Health - AI-Powered Health Analysis',
  description: 'AI-powered personal health intelligence for biomarker analysis, behavior change, and longitudinal wellness guidance.',
  keywords: 'health analysis, AI health, biomarkers, wellness, precision health',
  authors: [{ name: 'Ganesh Shinde' }],
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: '#667eea',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="font-sans antialiased">
        <AuthProvider>
          <ClientWarmUp />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
