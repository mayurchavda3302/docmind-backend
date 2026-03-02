import datetime
import logging
import os  # noqa: F401
import uuid  # noqa: F401

import inngest
import inngest.fast_api
from dotenv import load_dotenv
from fastapi import FastAPI
from inngest.experimental import ai  # noqa: F401

inject_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer(),
)

load_dotenv()


@inject_client.create_function(
    fn_id="RAG : Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/ingest_pdf"),
)
async def ingest_pdf(ctx: inngest.Context):
    return {
        "message": "PDF ingested successfully",
        "timestamp": datetime.datetime.now().isoformat(),
    }


app = FastAPI()


@app.get("/path_name")
async def method_name():
    pass


inngest.fast_api.serve(app, inject_client, functions=[ingest_pdf])
