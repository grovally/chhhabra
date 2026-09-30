from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.contact import router as contact_router
from routers.auth import router as auth_router
from routers.blog import router as blog_router


app = FastAPI(
    title="chhabra  API"
)


# ==============================
# CORS
# ==============================

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        # Production website
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
        "message": "chhabra server is running"
    }


# ==============================
# HEALTH CHECK
# ==============================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
@app.get("/")
def home():

    return {
        "message": "Chhabra Properties server is running"
    }


@app.get("/sitemap.xml")
def sitemap_xml():

    blogs = blogs_collection.find(
        {"published": True}
    ).sort(
        "createdAt",
        -1
    )

    urls = []
    for blog in blogs:
        slug = blog.get("slug")
        if slug:
            urls.append(
                f"<url><loc>https://chhabra-properties.com/blog/{slug}</loc></url>"
            )

    xml = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
{items}
</urlset>
""".format(items="\n".join(urls))

    return Response(content=xml, media_type="application/xml")
