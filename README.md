# ddos-switch
in case of DDOS attack on some IP address the service on that IP should be handed to another IP
and then the attacked IP should be blackholed to take off a load 

this fastapi based web service performs just that certain task  
Task is devided on three subtasks:
1. Dynamic DNS update
2. wait TTL seconds
3. Blackholing (RTHB) the old IP

there is just one route (api endpoint): *"/api/ddos"* with only **POST** method applied  
the payload must much the following data model:

```python
class Data(BaseModel):
    name: str
    prim_IP: IPv4Address
    subst_IP: IPv4Address
    TSIG: str
    ddos: bool = True
```
