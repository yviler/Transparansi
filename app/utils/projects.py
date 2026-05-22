from app.models.projects import Projects
from app.models.users import Users

from app.database import AsyncSession
from sqlalchemy import select

async def createProjectList(db: AsyncSession) -> list:
    return (await db.execute(select(Projects))).scalars().all()    