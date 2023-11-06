from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


tags_metadata = [
    {
        "name": "JOLP",
        "description": "api 목록",
    },
]


app = FastAPI(title="jolp Server API", openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,2
    allow_methods=["*"],
    allow_headers=["*"],
)



