import { Inter } from "next/font/google";
import Header from "./_components/Header";
import "./globals.css";

const sans = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "LatentScience",
  description:
    "AI-enabled service to help you identify scientific research which solves your query. ",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${sans.className} antialiased min-h-screen flex flex-col relative`}
      >
        <Header />

        <div className="relative flex-1 px-12 py-6 grid overflow-hidden">
          <div className="absolute inset-0 bg-white/40 -z-10" />

          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
