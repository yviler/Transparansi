from app.models.projects import Projects, Tasks
from app.models.users import Users
from app.database import AsyncSession
from sqlalchemy import select

async def createProjectList(db: AsyncSession) -> list:
    return (await db.execute(select(Projects))).scalars().all()    

async def insertProject(db: AsyncSession, project: Projects) -> None:
    db.add(project)
    await db.commit()

async def getProject(db: AsyncSession, project_id: str) -> Projects:
    return (await db.execute(select(Projects).where(Projects.id == project_id))).scalars().first

async def getProjectByName(db: AsyncSession, project_name: str) -> Projects:
    return (await db.execute(select(Projects).where(Projects.project_name == project_name))).scalars().first()

async def getProjectTasks(db: AsyncSession, project_id: str) -> tuple[Tasks]:
    return (await db.execute(select(Tasks).where(Tasks.projectID == project_id))).scalars().all()