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


@app.get("/api/user", response_model=schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
    return user


@app.get("/api/user_info", response_model=schemas.UserInfo)
async def get_user_info(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_user_info(user, db_session)


@app.post("/api/users")
async def create_user(
    user: schemas.UserCreate,
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    user_db = await services.get_user_by_email(user.email, db_session)
    if user_db:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use.")

    user = await services.create_user(user, db_session)

    return await services.create_token(user)


@app.put("/api/users", status_code=200)
async def update_user(
    user_update: schemas.UserUpdate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    await services.update_user(user_update, user, db_session)
    return {"message", "Successfully Updated."}


@app.post("/api/token")
async def generate_token(
    form_data: fastapi.security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    user = await services.authenticate_user(
        form_data.username, form_data.password, db_session
    )

    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials.")

    return await services.create_token(user)


@app.get("/api/students", response_model=List[schemas.Student])
async def get_students(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_students(user=user, db_session=db_session)


@app.get("/api/students/{student_id}", status_code=200)
async def get_student(
    student_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_student(student_id, user, db_session)


@app.post("/api/students", response_model=schemas.Student)
async def create_student(
    student: schemas.StudentCreate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.create_student(
        user=user, db_session=db_session, student=student
    )


@app.put("/api/students/{student_id}", status_code=200)
async def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    await services.update_student(student_id, student, user, db_session)
    return {"message", "Successfully Updated."}


@app.delete("/api/students/{student_id}", status_code=204)
async def delete_student(
    student_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    await services.delete_student(student_id, user, db_session)
    return {"message", "Successfully Deleted."}


@app.get("/api/images", response_model=List[schemas.Image])
async def get_images(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_images(user=user, db_session=db_session)


@app.get("/api/images/{image_id}", status_code=200)
async def get_image(
    image_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_image(image_id, user, db_session)


@app.get("/api/images_faces/{image_id}", status_code=200)
async def get_image_faces(
    image_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_image_faces(image_id, user, db_session)


@app.post("/api/images", response_model=schemas.Image)
async def create_image(
    image: schemas.ImageCreate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.create_image(user=user, db_session=db_session, image=image)


@app.delete("/api/images/{image_id}", status_code=204)
async def delete_image(
    image_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    await services.delete_image(image_id, user, db_session)
    return {"message", "Successfully Deleted."}


@app.post("/api/create_match_faces", status_code=200)
async def create_match_faces(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    await services.create_match_faces(user, db_session)
    return {"message", "Successfully finished matcheing all faces."}


@app.get("/api/get_match_faces", status_code=200)
async def get_match_faces(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_match_faces(user, db_session)


@app.post("/api/reports", status_code=200)
async def create_reports(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.create_update_reports(user=user, db_session=db_session)


@app.put("/api/reports", status_code=200)
async def update_reports(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.create_update_reports(user=user, db_session=db_session)


@app.get("/api/reports_info", status_code=200)
async def get_reports_info(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_reports_info(user=user, db_session=db_session)


@app.get("/api/reports", status_code=200)
async def get_reports(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_reports(user=user, db_session=db_session)


@app.get("/api/report/{report_id}", status_code=200)
async def get_report(
    report_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    return await services.get_specific_report(
        report_id=report_id, user=user, db_session=db_session
    )


@app.delete("/api/report/{report_id}", status_code=204)
async def delete_report(
    report_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    await services.delete_report(report_id, user, db_session)
    return {"message", "Successfully Deleted."}


@app.put("/api/report/{report_id}", status_code=200)
async def update_report(
    report_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db_session: orm.Session = fastapi.Depends(services.get_db_session),
):
    await services.update_report(report_id, user, db_session)
    return {"message", "Successfully Updated."}


@app.get("/api")
async def root():
    return {"message": "Social Relationships API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
