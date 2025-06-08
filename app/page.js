"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import Cover from "./_components/Cover";
import Main from "./_components/Main";

export default function App() {
  const router = useRouter();
  const [status, setStatus] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleNext = () => {
    setStatus((status) => status + 1);
  };

  // data is what the user inputs from the frontend
  const [data, setData] = useState({
    query: "",
    abstract: "",
  });

  // papers is what the backend sends to the frontend to display
  const [papers, setPapers] = useState({
    title1: "",
    abstract1: "",
    title2: "",
    abstract2: "",
    title3: "",
    abstract3: "",
  });

  const handleDataChange = useCallback((field, value) => {
    setData((prev) => ({
      ...prev,
      [field]: value,
    }));
  }, []);

  const handlePapersChange = useCallback((field, value) => {
    setPapers((prev) => ({
      ...prev,
      [field]: value,
    }));
  }, []);

  // Function to communicate with Modal backend
  const handleCompute = async (dataToSend = data) => {
    setLoading(true);
    
    try {
      // Replace with your actual Modal API endpoint URL (TODO)
      const MODAL_API_URL = process.env.NEXT_PUBLIC_MODAL_API_URL || 
        "https://your-app-name--api-endpoint.modal.run";

      const response = await fetch(`${MODAL_API_URL}/api/search-papers`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          paper: {
            title: "User Query Paper", // You might want to generate this
            abstract: dataToSend.abstract,
            authors: [],
          },
          research_question: {
            question: dataToSend.query,
            context: dataToSend.abstract,
          },
          max_results: 3, // We want 3 similar papers
          similarity_threshold: 0.7,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      // Update papers state with the results
      if (result && result.length >= 3) {
        handlePapersChange("title1", result[0].title || "");
        handlePapersChange("abstract1", result[0].abstract || "");
        handlePapersChange("title2", result[1].title || "");
        handlePapersChange("abstract2", result[1].abstract || "");
        handlePapersChange("title3", result[2].title || "");
        handlePapersChange("abstract3", result[2].abstract || "");
      }

      // Move to next screen after successful API call
      handleNext();
      
      // Clear the abstract field as requested
      handleDataChange("abstract", "");

    } catch (error) {
      console.error("API request error:", error);
      router.push("/error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-lg">
            <div className="text-xl font-bold">Processing your request...</div>
          </div>
        </div>
      )}

      <div className={status === 0 ? "" : "hidden"}>
        <Cover
          handleDataChange={handleDataChange}
          handleNext={handleNext}
          handleCompute={handleCompute}
          data={data}
        />
      </div>

      <div className={status === 1 ? "" : "hidden"}>
        <Main
          handleDataChange={handleDataChange}
          handleCompute={handleCompute}
          data={data}
          papers={papers}
        />
      </div>
    </>
  );
}