import Card from "./Card";

export default function Main({
  data,
  papers,
  handleDataChange,
  handleCompute,
}) {
  return (
    <>
      <div className="w-[1400px] h-[650px] flex">
        <div className="flex flex-1">
          <Card
            title={papers.title1 || "Loading..."}
            abstract={papers.abstract1 || "Fetching related papers..."}
            handleDataChange={handleDataChange}
            handleCompute={handleCompute}
          />
          <Card
            title={papers.title2 || "Loading..."}
            abstract={papers.abstract2 || "Fetching related papers..."}
            handleDataChange={handleDataChange}
            handleCompute={handleCompute}
          />
          <Card
            title={papers.title3 || "Loading..."}
            abstract={papers.abstract3 || "Fetching related papers..."}
            handleDataChange={handleDataChange}
            handleCompute={handleCompute}
          />
        </div>
      </div>
    </>
  );
}