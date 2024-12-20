from fastapi import FastAPI
from flowx_backend.core.event import startup_event, shutdown_event
from flowx_backend.api.token  import token_api
from flowx_backend.api.user import user_api
from flowx_backend.api.auth import auth_api
from contextlib import asynccontextmanager
from flowx_backend.core.config import settings
from flowx_backend.core.cors_config import setup_cors
from flowx_backend.core.middleware import AuthMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect db
    await startup_event()
    yield
    # disconnect db
    await shutdown_event()


app = FastAPI(lifespan=lifespan)


# app.middleware(JWTAuthMiddleware) #type: ignore
# app.add_middleware(AuthMiddleware)
setup_cors(app)


# app.add_event_handler("startup", startup_event)
# app.add_event_handler("shutdown", shutdown_event)

app.include_router(token_api.router, prefix=settings.API_VERSION, tags=["token"])
app.include_router(user_api.router, prefix=settings.API_VERSION, tags=["users"])
app.include_router(auth_api.router, prefix=settings.API_VERSION, tags=["auth"])

