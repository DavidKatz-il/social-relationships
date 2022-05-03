from typing import List

import fastapi
import uvicorn
from sqlalchemy import orm

from app import schemas, services


app = fastapi.FastAPI(
    title="Social Relationships - API",
)


@app.on_event("startup")
async def startup():
    services.create_database()


@app.get("/api/users/user", response_model=schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
    return user


@app.post("/api/users")
async def create_user(
    user: schemas.UserCreate, db: orm.Session = fastapi.Depends(services.get_db)
):
    user_db = await services.get_user_by_email(user.email, db)
    if user_db:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use.")

    user = await services.create_user(user, db)

    return await services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: fastapi.security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    user = await services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials.")

    return await services.create_token(user)


@app.get("/api/persons", response_model=List[schemas.Person])
async def get_persons(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.get_persons(user=user, db=db)


@app.get("/api/persons/{person_id}", status_code=200)
async def get_person(
    person_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.get_person(person_id, user, db)


@app.post("/api/persons", response_model=schemas.Person)
async def create_person(
    person: schemas.PersonCreate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.create_person(user=user, db=db, person=person)


@app.put("/api/persons/{person_id}", status_code=200)
async def update_person(
    person_id: int,
    person: schemas.PersonCreate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    await services.update_person(person_id, person, user, db)
    return {"message", "Successfully Updated."}


@app.delete("/api/persons/{person_id}", status_code=204)
async def delete_person(
    person_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    await services.delete_person(person_id, user, db)
    return {"message", "Successfully Deleted."}


@app.get("/api/images", response_model=List[schemas.Image])
async def get_images(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.get_images(user=user, db=db)


@app.get("/api/images/{image_id}", status_code=200)
async def get_image(
    image_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.get_image(image_id, user, db)


@app.post("/api/images", response_model=schemas.Image)
async def create_image(
    image: schemas.ImageCreate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.create_image(user=user, db=db, image=image)


@app.delete("/api/images/{image_id}", status_code=204)
async def delete_image(
    image_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    await services.delete_image(image_id, user, db)
    return {"message", "Successfully Deleted."}


@app.post("/api/create_match_faces", status_code=200)
async def create_match_faces(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    await services.create_match_faces(user, db)
    return {"message", "Successfully finished matcheing all faces."}

@app.get("/api/get_match_faces", status_code=200)
async def get_match_faces(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.get_match_faces(user, db)


@app.get("/api")
async def root():
    return {"message": "Social Relationships API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
