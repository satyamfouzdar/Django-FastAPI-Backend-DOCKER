from fastapi import APIRouter

router = APIRouter()

# Add apps routes like this.
# router.include_router(blog_router, prefix="/blog", tags=["Blog"])