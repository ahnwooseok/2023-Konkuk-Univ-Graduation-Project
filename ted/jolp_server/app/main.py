from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import lib.router as router


tags_metadata = [
    {
        "name": "JOLP",
        "description": "api 목록",
    },
]


app = FastAPI(title="jolp Server API", openapi_tags=tags_metadata)
app.include_router(router.router)



