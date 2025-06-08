from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from latentscience.model.paper import PaperSearchRequest, PaperSearchResponse
from latentscience.service.explanation import ExplanationService
from latentscience.service.paper import PaperService


router = APIRouter(tags=["paper"], route_class=DishkaRoute)


@router.post("/search")
async def search_similar_papers(
    request: PaperSearchRequest,
    paper_service: FromDishka[PaperService],
    explanation_service: FromDishka[ExplanationService],
) -> PaperSearchResponse:
    similar_papers = await paper_service.find_similar_papers(
        request.query, request.abstract
    )
    explanation = await explanation_service.explain_connection(
        request, similar_papers[0]
    )

    return PaperSearchResponse(papers=similar_papers, top_paper_comparison=explanation)


# @router.put("/")
# async def store_paper(request: PaperSubmitRequest): ...
