"""
Main module
"""
import uvicorn
from fastapi import FastAPI
from app.api.routes import routers
from app.utils.design_patterns import singleton


@singleton
class AppCreator:
    """
    App Creator class
    """
    def __init__(self):
        self.app = FastAPI()

        @self.app.get("/")
        def test():
            """
            root view
            """
            return '{"response": "Welcome to our clients portal!"}'

        self.app.include_router(routers, prefix="/api")


# Setup the application
app_creator = AppCreator()
app = app_creator.app

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
