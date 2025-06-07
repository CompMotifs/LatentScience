"use client";

import { useCallback, useState } from "react";
import Cover from "./_components/Cover";
import Main from "./_components/Main";

export default function App() {
  const [status, setStatus] = useState(0);
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

  // This is the function which communicates with the backend, you need to send the variable "data" over to the python script,
  // and return the three papers to display, set the values of the variable "papers" to the output using the function "handlePapersChange".
  // const handleCompute = async (e) => {
  //   e.preventDefault();
  //   // You send the POST request to the backend here, and receive the output of the Python file as json.

  //   if (error) {
  //     console.error("POST request error:", error);
  //     router.push("/error");
  //   } else {
  //     // if request successful
  //     // You should use function "setPapers" to modify the value of papers here.
  //     handleDataChange("abstract", ""); // set abstract field of user input to empty string.
  //   }
  // };

  return (
    <>
      <div className={status === 0 ? "" : "hidden"}>
        <Cover
          handleDataChange={handleDataChange}
          handleNext={handleNext}
          data={data}
          // handleCompute={handleCompute}
        />
      </div>

      <div className={status === 1 ? "" : "hidden"}>
        <Main
          handleDataChange={handleDataChange}
          data={data}
          papers={papers}
          // handleCompute={handleCompute}
        />
      </div>
    </>
  );
}
