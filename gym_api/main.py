import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.users import router as user_router
from .routers.tasks import router as task_router
from .routers.task_groups import router as tg_router
from .routers.exercises import router as ex_router


app = FastAPI()
origins = [
    "*",
    "https://localhost:3000",
    "http://localhost:3000",
    "https://127.0.0.1:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=user_router, prefix='/gym', tags=['user'])
app.include_router(router=task_router, prefix='/gym', tags=['task'])
app.include_router(router=tg_router, prefix='/gym', tags=['task_group'])
app.include_router(router=ex_router, prefix='/gym', tags=['exercises'])

def run():
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=3000,
        # ssl_certfile='/home/vasiliy/code/gym/gym/cert/cert.pem',
        # ssl_keyfile='/home/vasiliy/code/gym/gym/cert/key.pem'
        )
