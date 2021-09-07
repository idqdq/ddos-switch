from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from ipaddress import IPv4Address
from tasks import doDNSUpdate, waitTTLsecs, blackHole
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from config import *

app = FastAPI()

class Data(BaseModel):
    name: str
    prim_IP: IPv4Address
    subst_IP: IPv4Address
    tsig_keyname: str
    tsig_secret: str
    ddos: bool = True
    

def planttasks(data, background_tasks):
    # 3 tasks:
    # 1 - DNS Update
    # 2 - wait for TTL (300) secs
    # 3 - make a scrapli call to RTHB prim_IP on the router

    background_tasks.add_task(doDNSUpdate, data=data)
    background_tasks.add_task(waitTTLsecs, ttl=TTL)
    background_tasks.add_task(blackHole, ip=data.prim_IP, ddos=data.ddos)


@app.post("/api/ddosornotddos")
async def ddosornotddos(data: Data, background_tasks: BackgroundTasks):
    try:
        planttasks(data, background_tasks)        
        return "tasks planted successfully"
    except:
        return ":x: something went wrong"

@app.get("/api/ddosornotddosjwt")
async def ddosornotddos(token: str, background_tasks: BackgroundTasks):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])     
        del payload["exp"]
        data = Data(**payload)

        try:
            planttasks(data, background_tasks)        
            return ":robot: tasks planted successfully"
        except: 
            return ":x: something went wrong"

    except:
        return ":x: token is not valid"


## JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/gettoken")
def gettoken(data: Data):

    newdata = { 
        "name": data.name,
        "prim_IP": str(data.prim_IP),
        "subst_IP": str(data.subst_IP),
        "tsig_keyname": data.tsig_keyname,
        "tsig_secret": data.tsig_secret,
        "ddos": data.ddos,
    }

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data=newdata, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# d = { "name": "acs", 
#       "prim_IP": "195.230.111.106",
#       "subst_IP": "82.202.189.51", 
#       "tsig_keyname": "acs.key", 
#       "tsig_secret": "fKwttnpfMaD10CKh0/QqV13sBiGUvRDtRTLbwTdxpbw=", 
#       "ddos": True
# }
