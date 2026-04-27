from fastapi import FastAPI
from fastapi_swagger import patch_fastapi
from .web.task_routers import router as tasks_router
from .web.user_routers import router as users_router

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, docs_url="/docs")
app.include_router(tasks_router)
app.include_router(users_router)
