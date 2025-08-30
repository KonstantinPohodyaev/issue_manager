from src.crud.base import BaseCRUD
from src.models.task import Task


class TaskCRUD(BaseCRUD):
    """
    CRUD operations for Task model.

    Inherits all methods from BaseCRUD:
        - get_all
        - get
        - create
        - update
        - delete
    """
    pass


task_crud = TaskCRUD(Task)
