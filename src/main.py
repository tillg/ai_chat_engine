import json
import logging
import os
import urllib.parse

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from utils import get_logger

logger_general = get_logger("main", logging.INFO)

load_dotenv()

BASE_URL_OF_LLM = os.getenv("BASE_URL")
logger_general.info(f"BASE_URL_OF_LLM: {BASE_URL_OF_LLM}")

COMPLETION_URL = "/v1/chat/completions"
COMPLETION_URL_OF_LLM = urllib.parse.urljoin(BASE_URL_OF_LLM, COMPLETION_URL)
logger_general.info(f"COMPLETION_URL_OF_LLM: {COMPLETION_URL_OF_LLM}")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = get_logger("LoggingMiddleware", logging.INFO)
        body = await request.body()
        logger.info(f"Incoming request: {request.method} {request.url} {body.decode()}")
        response = await call_next(request)
        return response


app = FastAPI()


# app.add_middleware(LoggingMiddleware)

@app.post(COMPLETION_URL)
async def chat_completion(incoming_request: Request):
    logger = get_logger(chat_completion.__name__, logging.INFO)
    logger.info(f"Received Completion Request")

    incoming_request_data = await incoming_request.json()
    logger.info(f"Data of incoming Request: {incoming_request_data}")

    # Create a new request used to be sent to LLM
    outgoing_request_data = incoming_request_data.copy()
    outgoing_request_data["stream"] = False
    logger.info(f"outgoing request data: {outgoing_request_data}")

    # Convert the Pydantic model to a dictionary for sending with requests.post
    # outgoing_request_as_dict = outgoing_request_data.dict()

    res = requests.post(COMPLETION_URL_OF_LLM, json=outgoing_request_data)
    logger.info(f"Response from LLM: {json.dumps(res.json(), indent=4)}")
    return res.json()
