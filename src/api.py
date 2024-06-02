import asyncio

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from g4f.client import Client
from g4f.Provider import HuggingChat

import fuzzy_json as fjson
from json import JSONDecodeError

from src.swears import SFilter
from src.utils import has_swear
from src.constants import get_prompt, MAX_QUERY_LEN


class QueryModel(BaseModel):
    query: str


client = Client()
router = APIRouter()

sf = SFilter()


@router.post("/search")
async def search_movie(query: QueryModel):
    query_text = query.query

    if len(query_text) > MAX_QUERY_LEN:
        raise HTTPException(status_code=413, detail="Query too long.")

    if has_swear(sf, query_text):
        raise HTTPException(status_code=406, detail="Bad query.")

    prompt = get_prompt(query_text)

    response = await asyncio.to_thread(
        client.chat.completions.create,
        model="command-r+",
        messages=[{"role": "user", "content": prompt}],
        provider=HuggingChat,
        stream=False,
        proxy=None,
        response_format=None,
        max_tokens=None,
        stop=None,
        api_key=None,
        ignored=None,
        ignore_working=False,
        ignore_stream=False
    )

    answer = response.choices[0].message.content.replace('\x00', '')

    try:
        result = fjson.loads(answer)
        return result
    except JSONDecodeError:
        try:
            error_code = int(answer)

            if error_code == 0:
                raise HTTPException(status_code=404, detail="Film not found.")
            elif error_code == 1:
                raise HTTPException(status_code=406, detail="Bad query.")
            elif error_code == 2:
                raise HTTPException(status_code=406, detail="Insufficient data in query.")
        except:
            raise HTTPException(status_code=500, detail=f"Unknown error.")
