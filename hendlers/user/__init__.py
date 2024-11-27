from aiogram import Router
from .start import router as start_router
from .other import router as other_router
from .settings import router as settings_router
from .donate import router as donate_router
from .request_to_ai import router as ai_router

router = Router()
router.include_routers(start_router,
                       settings_router,
                       donate_router,
                       other_router,
                       ai_router)