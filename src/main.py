from fastapi import FastAPI

from src.api.routers import main_router
from src.core.config import settings


APP_DESCRIPTION = """
This API allows you to manage tasks:  
- Create tasks  
- Retrieve tasks  
- Update tasks  
- Delete tasks  

## Models
- **Task** has:

  - `uuid` — unique identifier  

  - `title` — short title  

  - `description` — optional details  
  
  - `status` — current state (`created`, `in_progress`, `done`)
"""


app = FastAPI(
    title=settings.fastapi_title,
    description=settings.fastapi_description or APP_DESCRIPTION,
    version='1.0.0',
    contact={
        "name": "Konstantin",
        "url": "https://github.com/KonstantinPohodyaev",
        "email": "konstantinpohodyaev@email.com",
    },
)
app.router.include_router(main_router)
