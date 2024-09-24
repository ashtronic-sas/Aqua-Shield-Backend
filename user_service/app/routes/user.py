from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserLogin , UserResponse,UserUpdate
from app.services.user_service import create_user, authenticate_user
from app.config.database import get_db
from app.auth.jwt_handler import create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from app.models.models import User
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
        "email": db_user.email
    }
    return UserResponse(message="User registered successfully", user=user_data)

@router.post("/login", response_model=Dict[str, str])
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
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{id}", response_model=UserOut)
def read_users(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    #User.username == current_user["sub"]

    current_user = get_current_user(token)
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{id}", response_model=UserOut)
def update_user(id: int, user: UserUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.username is not None:
        db_user.username = user.username
    if user.password is not None:
        db_user.password = user.password
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{id}", response_model=Dict[str, str])
def delete_user(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.get("", response_model=List[UserOut])
def read_users_all(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Lee todos los usuarios registrados en el sistema.

    Args:
        token (str, opcional): El token de autenticación proporcionado por el esquema OAuth2. Por defecto es Depends(oauth2_scheme).
        db (Session, opcional): La sesión de la base de datos. Por defecto es Depends(get_db).

    Returns:
        List[UserOut]: La información de todos los usuarios registrados en el sistema.
    """
    users = db.query(User).all()

    return users