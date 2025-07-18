import type { Metadata } from "next";
import { NextIntlClientProvider, hasLocale } from "next-intl";
import { notFound, redirect } from "next/navigation";
import { routing } from "@/i18n/routing";
import "@/app/globals.css";
import TopBar from "@/components/TopBar";
import Navbar from "@/components/NavBar";
import Footer from "@/components/Footer";
import { Toaster } from "@/components/ui/sonner";
import FacebookPixel from '../../components/FacebookPixel'
export const metadata: Metadata = {
  title: "TIFT",
  description: "TIFT university",
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon.ico',
    apple: '/favicon.ico', // You can also add an apple-touch-icon.png for better iOS support
  },
};

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  // Ensure that the incoming `locale` is valid
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) {
    notFound();
  }
  if (!['uz', 'ru'].includes(locale)) {
    redirect('/uz');
  }

  return (
    <html lang={locale}>
      <link rel="icon" href="/favicon.ico" sizes="any" />
      <body className="flex min-h-screen flex-col">
        <FacebookPixel />
        <NextIntlClientProvider>
          <TopBar />
          <Navbar />
          <main className="flex-grow pb-10 bg-gray-50">{children}</main>
          <Footer />
          <Toaster
            // richColors
            position="top-right"
          />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
