from contextlib import asynccontextmanager

from fastapi import FastAPI

from .analysis.models import HistoryAnalysis, TradeAnalysis  # noqa: F401
from .core.database import create_table
from .core.exceptions import APIException, global_api_exception_handler
from .entries.models import Entries  # noqa: F401
from .payments.models import Subscription  # noqa: F401
from .users.models import Users  # noqa: F401
from .users.routes import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


version = "v1"

app = FastAPI(
    title="Echolog API",
    version=version,
    description="EchoLog is a meticulously structured REST API that transforms daily journaling into actionable insights",
    lifespan=lifespan,
)

# Exception handlers
app.add_exception_handler(APIException, global_api_exception_handler)

# Include routers
app.include_router(auth_router, prefix=f"/api/{version}")
app.include_router(user_router, prefix=f"/api/{version}")
