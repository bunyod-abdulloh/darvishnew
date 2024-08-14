from aiogram import Router

from bot.filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .users import (start, courses_main_hr, articles_hr, projects, projects_two, testshr, ayzenktemperamenthr,
                        testleongard)
    from .errors import error_handler
    from .admin import admin_main, admin_users, admin_downloads, xlsx_to_sql, get_ids

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))
    #  Users
    router.include_routers(start.router, error_handler.router, courses_main_hr.courses, articles_hr.articles,
                           projects.interviews_projects, projects_two.router, testshr.test, ayzenktemperamenthr.router,
                           testleongard.router)
    # Admins
    router.include_routers(admin_main.router, admin_users.router, admin_downloads.router, xlsx_to_sql.router,
                           get_ids.router)
    return router
