import Card from "./Card";

const papers_placeholder = {
  title1: "Extracellular vesicle heterogeneity through the lens of multiomics",
  abstract1:
    "Silva and colleagues refine an EV isolation method to optimize recovery of cancer-derived large oncosomes (LOs). This approach enables high-yield profiling by mass spectrometry and bulk/single-LO RNA-seq. A consistent set of credentialed proteins is enriched in LOs from various cancer sources, including patient plasma.",
  title2: "A neural basis for distinguishing imagination from reality",
  abstract2:
    "Dijkstra et al. show that our brain distinguishes imagination from reality by monitoring how strongly the fusiform gyrus is activated. When imagined and real images produce similar activity, people can confuse them. This helps explain how we normally tell what is real—and why that sometimes fails.",
  title3:
    "End-to-end topographic networks as models of cortical map formation and human visual behaviour",
  abstract3:
    "Lu et al. introduce all-topographic neural networks as a parsimonious model of the human visual cortex.",
};

export default function Main({
  data, // contains the query from the landing page, and an empty abstract which will be filled by one of the three paper's abstract depending on user choice
  papers, // papers should contain the content which needs to be rendered, it should have the same format as papers_placeholder
  handleDataChange,
  handleCompute,
}) {
  return (
    <>
      <div className="w-[1400px] h-[650px] flex">
        <div className="flex flex-1">
          <Card
            title={papers_placeholder.title1} // replace papers_placeholder with "papers"
            abstract={papers_placeholder.abstract1}
            handleDataChange={handleDataChange}
            // handleCompute={handleCompute}
          />
          <Card
            title={papers_placeholder.title2}
            abstract={papers_placeholder.abstract2}
            handleDataChange={handleDataChange}
            // handleCompute={handleCompute}
          />
          <Card
            title={papers_placeholder.title3}
            abstract={papers_placeholder.abstract3}
            handleDataChange={handleDataChange}
            // handleCompute={handleCompute}
          />
        </div>
      </div>
    </>
  );
}
