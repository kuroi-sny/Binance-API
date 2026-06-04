from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, database
from database import get_db

## AUTH tools
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "Super_super_secret_key"
ALGORITHM = "HS256" 

## Command sqlalchemy to build all the tables in the database rn
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/signup")
def create_user(request:schemas.UserCreate, db: Session = Depends(get_db)):
    
    scramble_password = pwd_context.hash(request.password)
    
    new_user = models.User(username=request.username, hashed_password = scramble_password)
    
    db.add(new_user)
    db.commit()
    return{"message":f"{request.username} account created successfuly!"}


@app.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.username == request.username).first()
    if db_user == None:
        raise HTTPException(status_code=404, detail= f"{db_user} not found") 
    is_correct = pwd_context.verify(request.password, db_user.hashed_password)

    if is_correct == False:
        raise HTTPException(status_code=401, detail = "Incorrect Passowrd!")
    if is_correct == True and db_user != None: 
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=30)
        payload = {"sub": request.username, "exp":expire_time }
        wristband = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



        return{"access_token": wristband, "token_type": "bearer"}

# 2. This tells the Bouncer where users go to get their wristbands
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 3. The Bouncer Function
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # The Bouncer checks the secret signature on the wristband
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # He reads the username written on it
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid wristband!")
            
        return username
        
    except jwt.PyJWTError:
        # If the signature is fake or expired, kick them out
        raise HTTPException(status_code=401, detail="Fake or expired wristband!")
 
@app.get("/portfolio")
def view_portfolio(current_user: str = Depends(get_current_user)):
    
    # If the code reaches this line, it means the Bouncer checked the wristband 
    # and it was 100% valid. The Bouncer also extracted the username for us!
    
    return {"message": f"Welcome to your private portfolio, {current_user}!"}
