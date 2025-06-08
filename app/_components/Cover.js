export default function Cover({
  data,
  handleDataChange,
  handleNext,
  handleCompute,
}) {
  
  const handleStartClick = async () => {
    // Validate input
    if (!data.query.trim() || !data.abstract.trim()) {
      alert("Please fill in both the query and abstract fields.");
      return;
    }

    // Call the API and then proceed to next screen
    await handleCompute();
  };

  return (
    <div>
      <p className="flex flex-col text-2xl mt-4 mb-8 text-slate-700">
        LatentScience is a scientific reasoning engine which helps you traverse
        academic literature to answer your scientific question. It identifies
        hidden links, shared concepts, and all that can help you accelerate your
        research.
      </p>
      <p className="flex flex-col text-2xl mb-8 text-slate-700">
        Start here by giving us your scientific question, and one abstract to
        get the algorithm going.
      </p>

      <input
        type="text"
        placeholder="Your scientific query goes here."
        maxLength={50}
        value={data.query}
        onChange={(e) => handleDataChange("query", e.target.value)}
        className="w-1/2 px-4 py-2 rounded-lg shadow-xl border-b-2 mb-8 border-b-slate-700 focus:outline-none focus:border-b-2 focus:border-b-purple-700 transition-all duration-300 ease-in-out transform focus:scale-105 origin-top-left"
      />

      <textarea
        placeholder="Your abstract goes here."
        maxLength={5000}
        value={data.abstract}
        onChange={(e) => handleDataChange("abstract", e.target.value)}
        rows={6}
        className="w-full px-4 py-3 rounded-lg shadow-xl border-2 mb-8 border-gray-300 focus:outline-none focus:border-purple-700 transition-all duration-300 ease-in-out"
      />

      <button
        onClick={handleStartClick}
        className="bg-purple-700 text-white text-[24px] font-bold px-6 py-2 rounded shadow-xl origin-top-left transition-transform duration-200 hover:scale-105 active:scale-95"
      >
        Start!
      </button>
    </div>
  );
}