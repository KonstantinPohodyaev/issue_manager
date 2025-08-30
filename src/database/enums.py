from enum import StrEnum


class StatusEnum(StrEnum):
    """
    Enum for task statuses.

    Attributes:
        CREATED (str): Task is newly created.
        IN_PROGRESS (str): Task is currently in progress.
        COMPLETED (str): Task has been completed.
    """
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
