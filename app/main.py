from fastapi import FastAPI
from app.routes.auth import router
from app.database import Base, engine
#from app.models import user

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router)


