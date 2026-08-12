import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? 'http://localhost:3000'),
  title: 'ScalePilot AI — Run and Scale Your Agency With AI',
  description: 'Create content, generate leads, automate outreach, manage clients, and scale campaigns with AI.',
  openGraph: {
    title: 'ScalePilot AI — Run and Scale Your Agency With AI',
    description: 'Create content, generate leads, automate outreach, manage clients, and scale campaigns with AI.',
    images: ['/og.png'],
  },
  twitter: { card: 'summary_large_image', images: ['/og.png'] },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
