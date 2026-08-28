from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.database import create_table
from .users.routes import user_router
from .entries.models import Entries
from .analysis.models import TradeAnalysis, HistoryAnalysis
from .payments.models import Subscription
from .users.models import Users


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(user_router, prefix=f"/api/{version}")
