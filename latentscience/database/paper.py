import psycopg2
from ..model.paper import Paper, SimilarPaper


class PaperRepository:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    async def find_similar_papers(
        self, embedding: list[float], threshold: float = 0.7
    ) -> list[SimilarPaper]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, abstract, field, embedding, 1 - (embedding <=> %s::vector) AS similarity_score
                FROM papers
                ORDER BY embedding <=> %s::vector
                LIMIT 10
                """,
                (embedding, embedding),
            )
            results = cursor.fetchall()
            return [
                SimilarPaper(
                    paper=Paper(
                        id=row[0],
                        title=row[1],
                        abstract=row[2],
                        field=row[3],
                        embedding=[],
                    ),
                    similarity_score=float(row[5]),
                )
                for row in results
            ]

    def insert(self, id: str, title: str, abstract: str, authors: list[str], year: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO papers (id, title, abstract, field, embedding)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id, title, abstract, ", ".join(authors), year),
            )
        self.conn.commit()

    def get_by_id(self, id: str) -> Paper | None:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, abstract, field, embedding
                FROM papers
                WHERE id = %s
                """,
                (id,),
            )
            result = cursor.fetchone()
            if result:
                return Paper(
                    id=result[0],
                    title=result[1],
                    abstract=result[2],
                    field="",  # Default empty field as database doesn't have this
                    embedding=[],  # Default empty embedding as database doesn't have this
                )
            return None

    def get_all(self) -> list[Paper]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, abstract, field, embedding
                FROM papers
                """
            )
            results = cursor.fetchall()
            return [
                Paper(
                    id=row[0],
                    title=row[1],
                    abstract=row[2],
                    field="",  # Default empty field as database doesn't have this
                    embedding=[],  # Default empty embedding as database doesn't have this
                )
                for row in results
            ]
