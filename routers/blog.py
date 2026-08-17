from fastapi import APIRouter, Depends, HTTPException

from datetime import datetime, timezone

from database import blogs_collection

from models.blog import BlogCreate, BlogUpdate

from utils.auth import verify_token


router = APIRouter(prefix="/api/blogs", tags=["Blogs"])


def serialize_blog(blog):

    return {
        "id": str(blog["_id"]),
        "title": blog["title"],
        "slug": blog["slug"],
        "description": blog["description"],
        "content": blog["content"],
        "category": blog["category"],
        "author": blog["author"],
        "image": blog["image"],
        "published": blog["published"],
        "createdAt": blog["createdAt"],
    }


def create_slug(title):

    return (
        title.lower()
        .strip()
        .replace(" ", "-")
        .replace("/", "-")
    )


# =========================
# PUBLIC BLOGS
# =========================

@router.get("/")
def get_blogs():

    blogs = blogs_collection.find(
        {"published": True}
    ).sort(
        "createdAt",
        -1
    )

    return [
        serialize_blog(blog)
        for blog in blogs
    ]


@router.get("/{slug}")
def get_blog(slug: str):

    blog = blogs_collection.find_one({
        "slug": slug,
        "published": True
    })

    if not blog:

        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return serialize_blog(blog)


# =========================
# ADMIN BLOGS
# =========================

@router.get("/admin/all")
def get_all_blogs(
    user=Depends(verify_token)
):

    blogs = blogs_collection.find().sort(
        "createdAt",
        -1
    )

    return [
        serialize_blog(blog)
        for blog in blogs
    ]


@router.post("/")
def create_blog(
    blog: BlogCreate,
    user=Depends(verify_token)
):

    slug = create_slug(blog.title)

    existing = blogs_collection.find_one({
        "slug": slug
    })

    if existing:

        slug = f"{slug}-{int(datetime.now().timestamp())}"

    blog_data = {
        "title": blog.title,
        "slug": slug,
        "description": blog.description,
        "content": blog.content,
        "category": blog.category,
        "author": blog.author,
        "image": blog.image,
        "published": blog.published,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    result = blogs_collection.insert_one(
        blog_data
    )

    blog_data["_id"] = result.inserted_id

    return serialize_blog(blog_data)


@router.put("/{blog_id}")
def update_blog(
    blog_id: str,
    blog: BlogUpdate,
    user=Depends(verify_token)
):

    from bson import ObjectId

    update_data = {
        key: value
        for key, value in blog.model_dump().items()
        if value is not None
    }

    if "title" in update_data:

        update_data["slug"] = create_slug(
            update_data["title"]
        )

    result = blogs_collection.update_one(
        {
            "_id": ObjectId(blog_id)
        },
        {
            "$set": update_data
        }
    )

    if result.matched_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    updated = blogs_collection.find_one({
        "_id": ObjectId(blog_id)
    })

    return serialize_blog(updated)


@router.delete("/{blog_id}")
def delete_blog(
    blog_id: str,
    user=Depends(verify_token)
):

    from bson import ObjectId

    result = blogs_collection.delete_one({
        "_id": ObjectId(blog_id)
    })

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return {
        "success": True,
        "message": "Blog deleted"
    }