export default function Card({
  title,
  abstract,
  handleDataChange,
  handleCompute,
}) {
  
  const handleCardClick = async () => {
    // Update the data with the selected abstract
    const updatedData = { abstract: abstract };
    handleDataChange("abstract", abstract);
    
    // Call the API with the updated data
    await handleCompute(updatedData);
  };

  return (
    <div className="relative border-3 border-purple-700 w-1/3 m-3 rounded-[4rem] shadow-2xl">
      <div className="absolute top-[3rem] left-[3rem] right-[3rem] bottom-[3rem] m-auto">
        <div className="text-xl font-bold mb-4">{title}</div>
        <div className="w-full h-px bg-slate-300 mb-4"></div>
        <div className="text-md mb-6">{abstract}</div>
        <button
          onClick={handleCardClick}
          className="bg-purple-700 text-white text-[16px] font-bold px-6 py-2 rounded shadow-xl origin-top-left transition-transform duration-200 hover:scale-105 active:scale-95"
        >
          This one is the most interesting.
        </button>
      </div>
    </div>
  );
}