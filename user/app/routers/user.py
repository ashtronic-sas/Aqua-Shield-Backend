from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserLogin , UserResponse,UserUpdate, UserAuthResponse
from app.services.user_service import create_user, authenticate_user,get_user_by_id,update_user_by_id,delete_user_by_id,get_all_users
from app.config.database import get_db
from app.auth.jwt_handler import create_access_token
from typing import Dict
from app.models.models import User
from typing import List
from app.shared.utils import verify_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, dependencies=[Depends(verify_token)])
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.

    Args:
        user (UserCreate): Objeto que contiene la información del usuario a crear.
        token (str, opcional): Token de autenticación proporcionado por el esquema OAuth2. Por defecto es Depends(oauth2_scheme).
        db (Session, opcional): Sesión de base de datos proporcionada por la dependencia get_db. Por defecto es Depends(get_db).

    Returns:
        UserResponse: Un objeto que contiene el token de acceso, el tipo de token, un mensaje de éxito y los datos del usuario creado.
    """
    db_user = create_user(user, db)

    user_data = {
        "id": str(db_user.id),
        "username": db_user.username,
    }
    return UserResponse(message="User registered successfully", user=user_data)

@router.post("/login", response_model=UserAuthResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Maneja el proceso de inicio de sesión de un usuario.

    Args:
        user (UserLogin): Objeto que contiene las credenciales del usuario.
        db (Session, opcional): Sesión de la base de datos proporcionada por la dependencia get_db. Por defecto es Depends(get_db).

    Returns:
        dict: Un diccionario que contiene el token de acceso y el tipo de token.

    Raises:
        HTTPException: Si las credenciales son inválidas, se lanza una excepción con el código de estado 401 y un mensaje de detalle.
    """
    return authenticate_user(db, user.username, user.password)

@router.get("/{id}", response_model=UserOut, dependencies=[Depends(verify_token)])
def read_users_id(id: int, db: Session = Depends(get_db)):
    """
    Lee la información del usuario actual basado en su ID y token de autenticación.

    Args:
        id (int): El ID del usuario.
        token (str, opcional): El token de autenticación proporcionado por el esquema OAuth2. Por defecto es Depends(oauth2_scheme).
        db (Session, opcional): La sesión de la base de datos. Por defecto es Depends(get_db).

    Returns:
        User: La información del usuario si se encuentra.

    Raises:
        HTTPException: Si el usuario no se encuentra, se lanza una excepción con código de estado 404 y un mensaje de "User not found".
    """
    return get_user_by_id(id, db)

@router.put("/{id}", response_model=UserOut, dependencies=[Depends(verify_token)])
def update_user_id(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información del usuario basado en su ID.

    Args:
        id (int): El ID del usuario a actualizar.
        user (UserUpdate): Objeto que contiene la nueva información del usuario.
        token (str, opcional): Token de autenticación del usuario. Por defecto se obtiene mediante Depends(oauth2_scheme).
        db (Session, opcional): Sesión de la base de datos. Por defecto se obtiene mediante Depends(get_db).

    Returns:
        User: Objeto de usuario actualizado.

    Raises:
        HTTPException: Si el usuario no se encuentra en la base de datos, se lanza una excepción con código de estado 404.
    """
    
    return update_user_by_id(id, user, db)

@router.delete("/{id}", response_model=Dict[str, str], dependencies=[Depends(verify_token)])
def delete_user_id(id: int, db: Session = Depends(get_db)):
    """
    Eliminar el usuario actual por ID.

    Args:
        id (int): El ID del usuario a eliminar.
        token (str, opcional): El token OAuth2 para autenticación. Por defecto es Depends(oauth2_scheme).
        db (Session, opcional): La sesión de la base de datos. Por defecto es Depends(get_db).

    Raises:
        HTTPException: Si el usuario no se encuentra, lanza una excepción HTTP 404.

    Returns:
        dict: Un diccionario que contiene un mensaje de éxito.
    """

    return delete_user_by_id(id, db)

@router.get("", response_model=List[UserOut], dependencies=[Depends(verify_token)])
def read_users_all(db: Session = Depends(get_db)):
    """
    Lee todos los usuarios registrados en el sistema.

    Args:
        token (str, opcional): El token de autenticación proporcionado por el esquema OAuth2. Por defecto es Depends(oauth2_scheme).
        db (Session, opcional): La sesión de la base de datos. Por defecto es Depends(get_db).

    Returns:
        List[UserOut]: La información de todos los usuarios registrados en el sistema.
    """
    

    return get_all_users(db)