from app.models.models import AdminUser, User
from app.schemas.admin_user import AdminUserCreate
from app.config.database import get_db
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Create a new admin user
def create_admin_user_new(admin_user: AdminUserCreate, db: Session):
    """
    Crea un nuevo usuario administrador en la base de datos.
    Args:
        admin_user (AdminUserCreate): Objeto que contiene la información del nuevo usuario administrador.
        db (Session): Sesión de la base de datos para realizar las operaciones.
    Raises:
        HTTPException: Si el correo electrónico ya está registrado.
        HTTPException: Si el nombre de usuario ya está registrado.
        HTTPException: Si el documento ya está registrado.
    Returns:
        AdminUser: El nuevo usuario administrador creado.
    """
    try:
        # Check if email already exists
        if db.query(AdminUser).filter(AdminUser.email == admin_user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Check if username already exists
        if db.query(User).filter(User.username == admin_user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if documento already exists
        if db.query(AdminUser).filter(AdminUser.documento == admin_user.documento).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Documento already registered"
            )

        # Encrypt the password
        hashed_password = pwd_context.hash(admin_user.password)

        new_user = User(
            username=admin_user.username,
            hashed_password=hashed_password
        )

        new_admin_user = AdminUser(
            email=admin_user.email,
            first_name=admin_user.first_name,
            second_name=admin_user.second_name,
            first_last_name=admin_user.first_last_name,
            second_last_name=admin_user.second_last_name,
            documento=admin_user.documento,
            photo=admin_user.photo,
            user=new_user
        )

        db.add(new_user)
        db.add(new_admin_user)
        db.commit()
        db.refresh(new_admin_user)

        return new_admin_user
    except HTTPException as e:
        return {"error": e.detail}
# Get all admin users
def get_admin_user_all(db: Session):
    """
    Obtiene todos los usuarios administradores de la base de datos.

    Args:
        db (Session): Sesión de la base de datos.

    Returns:
        List[AdminUser]: Lista de todos los usuarios administradores.
    """
    return db.query(AdminUser).all()

def get_admin_user_id(id: int, db: Session):
    """
    Obtiene un usuario administrador de la base de datos.
    Parámetros:
    id (int): El ID del usuario administrador a obtener.
    db (Session): La sesión de la base de datos.
    Excepciones:
    HTTPException: Si no se encuentra un usuario administrador con el ID proporcionado.
    Retorna:
    AdminUser: El usuario administrador con el ID especificado.
    """
    admin_user = db.query(AdminUser).filter(AdminUser.id == id).first()
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin user with id {id} not found"
        )
    return admin_user

# Delete an admin user
def delete_admin_user_db(id: int, db: Session):
    """
    Elimina un usuario administrador de la base de datos.
    Parámetros:
    id (int): El ID del usuario administrador a eliminar.
    db (Session): La sesión de la base de datos.
    Excepciones:
    HTTPException: Si no se encuentra un usuario administrador con el ID proporcionado.
    Retorna:
    AdminUser: El usuario administrador eliminado.
    """
    admin_user = db.query(AdminUser).filter(AdminUser.id == id).first()
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin user with id {id} not found"
        )
    
    # Delete the associated user
    user = db.query(User).filter(User.id == admin_user.user_id).first()
    if user:
        db.delete(user)
    
    db.delete(admin_user)
    db.commit()
    return admin_user
# Update an admin user
def update_admin_user_db(id: int, admin_user: AdminUserCreate, db: Session):
    """
    Actualiza un usuario administrador en la base de datos.
    Args:
        id (int): El ID del usuario administrador a actualizar.
        admin_user (AdminUserCreate): Los nuevos datos del usuario administrador.
        db (Session): La sesión de la base de datos.
    Raises:
        HTTPException: Si el usuario administrador con el ID especificado no se encuentra.
        HTTPException: Si el correo electrónico ya está registrado.
        HTTPException: Si el documento ya está registrado.
    Returns:
        AdminUser: El usuario administrador actualizado.
    """

    admin_user_db = db.query(AdminUser).filter(AdminUser.id == id).first()
    if not admin_user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin user with id {id} not found"
        )

    # Check if email already exists
    if db.query(AdminUser).filter(AdminUser.email == admin_user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if documento already exists
    if db.query(AdminUser).filter(AdminUser.documento == admin_user.documento).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Documento already registered"
        )

    # Encrypt the password

    user = db.query(User).filter(User.id == admin_user_db.user_id).first()
    if admin_user.username:
        user.username = admin_user.username
    if admin_user.password:
        hashed_password = pwd_context.hash(admin_user.password)
        user.hashed_password = hashed_password
    if admin_user.email:
        admin_user_db.email = admin_user.email
    if admin_user.first_name:
        admin_user_db.first_name = admin_user.first_name
    if admin_user.second_name:
        admin_user_db.second_name = admin_user.second_name
    if admin_user.first_last_name:
        admin_user_db.first_last_name = admin_user.first_last_name
    if admin_user.second_last_name:
        admin_user_db.second_last_name = admin_user.second_last_name
    if admin_user.documento:
        admin_user_db.documento = admin_user.documento
    if admin_user.photo:
        admin_user_db.photo = admin_user.photo

    db.commit()
    db.refresh(admin_user_db)

    return admin_user_db






