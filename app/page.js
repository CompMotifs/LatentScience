"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function App() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [abstract, setAbstract] = useState("");
  const handleQuery = (text) => {
    setQuery(text);
  };
  const handleAbstract = (text) => {
    setAbstract(text);
  };

  const handleStart = async (e) => {
    e.preventDefault();
    // THIS LINE IS WHERE YOU WILL SEND THE POST REQUEST WITH THE USER'S INPUT

    if (error) {
      console.error("POST request error:", error);
      router.push("/error");
    } else {
      router.push("/search");
    }
  };

  return (
    <div>
      <p className="flex flex-col text-2xl mt-4 mb-8 text-slate-700">
        LatentScience is a scientific reasoning engine which helps you traverse
        the whole academic literature to answer your scientific question. It
        identifies hidden links, shared concepts, and all that can help you
        accelerate your research.
      </p>
      <p className="flex flex-col text-2xl mb-8 text-slate-700">
        Start here by giving us your scientific question, and one abstract to
        get the algorithm going.
      </p>

      <input
        type="email"
        placeholder="Your scientific query goes here."
        maxLength={50}
        value={query}
        onChange={(e) => handleQuery(e.target.value)}
        className=" w-1/2 px-4 py-2 rounded-lg shadow-xl border-b-2 mb-8 border-b-gray-700 focus:outline-none focus:border-b-2 focus:border-b-purple-700 transition-all duration-300 ease-in-out transform focus:scale-105 origin-top-left"
      />

      <textarea
        placeholder="Your abstract goes here."
        maxLength={5000}
        value={abstract}
        onChange={(e) => handleAbstract(e.target.value)}
        rows={6}
        className="w-full px-4 py-3 rounded-lg shadow-xl border-2 mb-8 border-gray-300 focus:outline-none focus:border-purple-700 transition-all duration-300 ease-in-out"
      />

      <button
        onClick={handleStart}
        className="bg-purple-700 text-white text-[24px] font-bold px-6 py-2 rounded shadow-xl origin-top-left transition-transform duration-200 hover:scale-105 active:scale-95"
      >
        Start!
      </button>
    </div>
  );
}
