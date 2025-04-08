import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Server, Config

from kvmworkflows.config.config import config
from kvmworkflows.web.router.router import router


app = FastAPI(
    title=config.app.title,
    openapi_url=config.app.openapi_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.cors.allowed_origins,
    allow_credentials=config.app.cors.allow_credentials,
    allow_methods=config.app.cors.allowed_methods,
    allow_headers=config.app.cors.allowed_headers,
)

app.include_router(router)


async def main():
    server = Server(
        config=Config(
            app=app,
            host=config.app.host,
            port=config.app.port,
        )
    )
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
