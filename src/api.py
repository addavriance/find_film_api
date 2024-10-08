from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Request
from requests.exceptions import ChunkedEncodingError

from src.models.hugging_face.chat import Client
from src.models.kinopoisk.search import Search
import fuzzy_json as fjson
from json import JSONDecodeError

from src.swears import SFilter
from src.utils import has_swear, get_enclosed_json
from src.constants import get_prompt, MAX_QUERY_LEN, MIN_QUERY_LEN


class QueryModel(BaseModel):
    query: str


client = Client()
search = Search()

router = APIRouter()

sf = SFilter()


@router.post("/search")
async def search_movie(request: Request, query: QueryModel):
    query_text = query.query

    country = request.headers["Country"] if "Country" in request.headers else "US"

    if len(query_text) < MIN_QUERY_LEN:
        raise HTTPException(status_code=400, detail="Query too short.")

    if len(query_text) > MAX_QUERY_LEN:
        raise HTTPException(status_code=413, detail="Query too long.")

    if has_swear(sf, query_text):
        raise HTTPException(status_code=406, detail="Bad query.")

    prompt = get_prompt(query_text, country)

    dialogue = client.create_dialogue()

    print(dialogue)

    cID = dialogue['conversationId']

    try:
        answer = client.send_message(cID, prompt)
    except ChunkedEncodingError:
        answer = client.get_answer_from_title(cID)

    client.delete_dialogue(cID)

    try:
        if len(answer) == 1:
            error_code = int(answer)

            if error_code == 0:
                raise HTTPException(status_code=404, detail="Film not found.")
            elif error_code == 1:
                raise HTTPException(status_code=406, detail="Bad query.")
            elif error_code == 2:
                raise HTTPException(status_code=406, detail="Insufficient data in query.")
        else:
            raw_json = get_enclosed_json(answer)
            result = fjson.loads(raw_json)

            if result["fn"] is None or result["fd"] is None:
                raise HTTPException(status_code=404, detail="Film not found.")

            result = search.get_film_data(result["fn"])

            return result

    except JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Unknown error.")
