import Link from "next/link";
import Image from "next/image";
import logo from "@/public/default-monochrome.svg";

export default function Header() {
  return (
    <header className="border-b-2 border-b-gray-100">
      <div className="border-4 border-white px-8 py-4 flex">
        <Link href="/">
          <Image
            src={logo}
            height="180"
            quality={100}
            width="450"
            alt="The Papertrove.ai logo"
          />
        </Link>
      </div>
    </header>
  );
}
