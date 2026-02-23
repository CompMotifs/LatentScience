export default function Card({
  title,
  abstract,
  similarity_score,
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
    <div className="relative border-3 border-purple-700 w-1/3 m-3 rounded-[4rem] shadow-2xl h-[500px]">
      <div className="absolute top-[3rem] left-[3rem] right-[3rem] bottom-[3rem] flex flex-col">
        <div className="text-xl font-bold mb-4">{title}</div>
        <div className="w-full h-px bg-slate-300 mb-4"></div>
        <div className="text-md mb-4 flex-1 overflow-y-auto pr-2">{abstract}</div>
        <div className="text-sm text-gray-600 mb-3">
          Similarity: {similarity_score ? (similarity_score * 100).toFixed(1) + '%' : 'N/A'}
        </div>
      </div>
    </div>
  );
}
