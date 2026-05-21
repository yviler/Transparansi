from app.models.projects import Projects
from app.database import AsyncSession

async def createProjectList(db: AsyncSession) -> list:
    #TODO: actually find the right thing
    return db.get_all(Projects)
    