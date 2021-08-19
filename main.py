import uvicorn
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from ipaddress import IPv4Address
from tasks import doDNSUpdate, waitTTLsecs, blackHole

TTL = 5


app = FastAPI()

class Data(BaseModel):
    name: str
    prim_IP: IPv4Address
    subst_IP: IPv4Address
    TSIG: str
    ddos: bool = True
    
@app.post("/api/ddos")
async def hideFromDDos(data: Data, background_tasks: BackgroundTasks):
    # 3 tasks:
    # 1 - DNS Update
    # 2 - wait for 300 sec
    # 3 - make a scrapli call to RTHB prim_IP on the router
    try:
        background_tasks.add_task(doDNSUpdate, data=data)
        background_tasks.add_task(waitTTLsecs, ttl=TTL)
        background_tasks.add_task(blackHole, ip=data.prim_IP, ddos=data.ddos)
        return "tasks planted successfully"
    except:
        return ":x: something went wrong"




