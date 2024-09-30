from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.admin_user import AdminUserOut, AdminUserCreate, AdminUserUpdate
from app.services.admin_user_service import create_admin_user_new, get_admin_user_all, delete_admin_user_db, update_admin_user_db,get_admin_user_id
from app.config.database import get_db
from app.shared.utils import verify_token

router = APIRouter(prefix="/admin_user", tags=["admin_user"])


@router.post("/", response_model=AdminUserOut,dependencies=[Depends(verify_token)])
def create_admin_user(admin_user: AdminUserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario administrador.

    Args:
        admin_user (AdminUserCreate): Objeto que contiene la información del nuevo usuario administrador.
        db (Session, opcional): Sesión de la base de datos. Por defecto, se obtiene mediante la dependencia get_db.

    Returns:
        AdminUser: El usuario administrador creado.
    """
    return create_admin_user_new(admin_user, db)

@router.get("/", response_model=list[AdminUserOut],dependencies=[Depends(verify_token)])
def read_admin_user_all(db: Session = Depends(get_db)):
    """
    Lee todos los usuarios administradores de la base de datos.

    Args:
        db (Session): Sesión de la base de datos proporcionada por la dependencia get_db.

    Returns:
        List[AdminUser]: Lista de todos los usuarios administradores.
    """
    return get_admin_user_all(db)

@router.get("/{id}", response_model=AdminUserOut,dependencies=[Depends(verify_token)])
def read_admin_user_by_id(id: int, db: Session = Depends(get_db)):
    """
    Lee un usuario administrador de la base de datos.

    Args:
        id (int): El ID del usuario administrador que se desea leer.
        db (Session, opcional): Sesión de la base de datos proporcionada por la dependencia get_db.

    Returns:
        AdminUser: El usuario administrador con el ID especificado.
    """
    return get_admin_user_id(id,db)

@router.delete("/{id}", response_model=AdminUserOut,dependencies=[Depends(verify_token)])
def delete_admin_user(id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario administrador de la base de datos.

    Args:
        id (int): El ID del usuario administrador que se desea eliminar.
        db (Session, opcional): Sesión de la base de datos proporcionada por la dependencia get_db.

    Returns:
        La respuesta de la función delete_admin_user_db que maneja la eliminación del usuario en la base de datos.
    """
    
    return delete_admin_user_db(id, db)

@router.put("/{id}", response_model=AdminUserOut,dependencies=[Depends(verify_token)])
def update_admin_user(id: int, admin_user: AdminUserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un usuario administrador en la base de datos.

    Args:
        id (int): El identificador único del usuario administrador a actualizar.
        admin_user (AdminUserCreate): Un objeto que contiene los nuevos datos del usuario administrador.
        db (Session, opcional): Sesión de la base de datos para realizar la operación. Por defecto, se obtiene con Depends(get_db).

    Returns:
        El resultado de la operación de actualización en la base de datos.
    """
    return update_admin_user_db(id, admin_user, db)






