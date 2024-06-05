from fastapi import FastAPI
from store.core.config import settings
from store.routers import api_router


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            version="0.0.1",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH,
            *args,
            **kwargs,
        )


app = App()
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
