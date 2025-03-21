import asyncio

from fastapi import FastAPI
from uvicorn import Server, Config
from kvmworkflows.config.config import config
from kvmworkflows.web.router.router import router


app = FastAPI(title=config.app.title)
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
