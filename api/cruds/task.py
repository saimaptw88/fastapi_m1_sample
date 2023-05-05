from typing import List, Tuple, Optional
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import api.models.task as task_model
import api.schemas.task as task_schema


async def get_tasks_with_done(db: AsyncSession):
  result: Result = await (
    db.execute(
      select (
        task_model.Task.id,
        task_model.Task.title,
        task_model.Done.id.isnot(None).label("done"),
      ).outerjoin(task_model.Done)
    )
  )
  return result.all()


async def get_task(
  db: AsyncSession,
  task_id: int
) -> Optional[task_model.Task]:
  result: Result = await db.execute(
    select(task_model.Task).filter(task_model.Task.id == task_id)
  )
  task: Optional[Tuple[task_model.Task]] = result.first()
  return task[0] if task is not None else None


async def create_task(
  db: AsyncSession,
  task_create: task_schema.TaskCreate
) -> task_model.Task:
  task = task_model.Task(**task_create.dict())

  db.add(task)
  await db.commit()
  await db.refresh(task)

  return task


async def upadte_task(
  db: AsyncSession,
  task_create: task_schema.TaskCreate,
  original: task_model.Task
) -> task_model.Task:
  original.title = task_create.title

  db.add(original)
  await db.commit()
  await db.refresh(original)

  return original
