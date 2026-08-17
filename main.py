from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.contact import router as contact_router
from routers.auth import router as auth_router
from routers.blog import router as blog_router


app = FastAPI(
    title="Chhabra Properties API"
)


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://chhabra-properties.com",
        "https://www.chhabra-properties.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# ROUTERS
# ==============================

app.include_router(
    contact_router,
    prefix="/api"
)

app.include_router(
    auth_router
)

app.include_router(
    blog_router
)


# ==============================
# HOME
# ==============================

@app.get("/")
def home():

    return {
        "message": "Chhabra Properties server is running"
    }
