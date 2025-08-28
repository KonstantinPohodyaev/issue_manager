from src.crud.base import BaseCRUD
from src.models.task import Task


class TaskCRUD(BaseCRUD):
    pass


task_crud = TaskCRUD(Task)
