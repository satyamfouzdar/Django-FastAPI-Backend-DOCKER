from fastapi import APIRouter
from accounts.routes import router as accounts_router

router = APIRouter()

# Add apps routes like this.
# router.include_router(blog_router, prefix="/blog", tags=["Blog"])

router.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])