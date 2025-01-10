import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.exercise import router as ex_router

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
app.include_router(router=ex_router, prefix='/exercise')

def run():
    # asyncio.run(main())

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=3000,
        # ssl_certfile='/home/vasiliy/code/gym/gym/cert/cert.pem',
        # ssl_keyfile='/home/vasiliy/code/gym/gym/cert/key.pem'
        )



