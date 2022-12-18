from app.services.database import create_database, get_db_session
from app.services.image import (
    create_image,
    delete_image,
    get_image,
    get_image_faces,
    get_images,
)
from app.services.report import (
    create_update_reports,
    delete_report,
    get_reports,
    get_reports_info,
    get_specific_report,
    update_report,
)
from app.services.student import (
    create_student,
    delete_student,
    get_student,
    get_students,
    update_student,
)
from app.services.user import (
    authenticate_user,
    create_token,
    create_user,
    get_current_user,
    get_user_info,
    update_user,
)
from app.services.utils.db import get_user_by_email
from app.services.utils.face_recognition import create_match_faces, get_match_faces
