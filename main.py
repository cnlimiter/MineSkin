import uvicorn

from bootstrap.application import create_app
from config.app import settings as app_config

app = create_app()


@app.get("/")
async def root():
    return "Welcome!"


if __name__ == "__main__":
    uvicorn.run(app="main:app", host=app_config.SERVER_HOST, port=app_config.SERVER_PORT)
