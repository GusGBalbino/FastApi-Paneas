from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from security import hash_password, verify_password
from jwt_handler import bearer_scheme, verify_token, create_access_token
from fastapi.security import HTTPAuthorizationCredentials
from shared.dependencies import get_db
from users.models.users_model import Users
from users.models.base_models import Login, UserResponse, UserUpdateRequest, UserCreateRequest

router = APIRouter(prefix="/users")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return verify_token(credentials)


@router.post("/create", tags=["Create a new user to access the platform."], response_model=UserResponse, status_code=201)
def create_user(user_request: UserCreateRequest, db: Session = Depends(get_db)) -> UserResponse:
    try:
        hashed_password = hash_password(user_request.password.get_secret_value())
        user = Users(**user_request.model_dump(exclude={"password"}), password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        if 'users_email_key' in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already in use")
        else:
            raise HTTPException(status_code=500, detail=f"Database error: {e.orig}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.post("/token", tags=["JWT Token."])
def autentication(login_data: Login, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", tags=["List all users on the database."],response_model=List[UserResponse])
def list_all_users(db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)) -> List[UserResponse]:
    try:
        return db.query(Users).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.put("/update/{user_id}", tags=["Edit a user by their ID."],response_model=UserResponse)
def update_user(user_id: int, user_request: UserUpdateRequest, 
                db: Session = Depends(get_db), 
                current_user: Users = Depends(get_current_user)) -> UserResponse:
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_request.model_dump(exclude_unset=True)

    if 'password' in update_data:
        hashed_password = hash_password(update_data['password'])
        update_data['password'] = hashed_password

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/delete/{user_id}", tags=["Delete a user by their ID."],status_code=200)
def delete_user(user_id: int, 
                db: Session = Depends(get_db), 
                current_user: Users = Depends(get_current_user)):
    try:
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"detail": "User deleted"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")