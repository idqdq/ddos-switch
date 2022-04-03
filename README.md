# ddos-switch
in case of DDOS attack on some IP address the service on that IP should be handed to another IP
and then the attacked IP should be blackholed to take off a load 

this fastapi based web service performs just that certain task  
Task is devided on three subtasks:
1. Dynamic DNS update
2. wait TTL seconds
3. Blackholing (RTHB) the old IP

there are three routes (api endpoints):  
  1.  */api/ddosornotddos* - **POST** method. The payload must much the following data model:

```python
class Data(BaseModel):
    name: str
    prim_IP: IPv4Address
    subst_IP: IPv4Address
    TSIG: str
    ddos: bool = True
```

  2. */api/ddosornotddosjwt?token=JWT* - **GET** method. It takes a **JWT** token that contains an encoded data (model Data)
  3. */api/gettoken* - **POST** method. It takes the data (model Data) and encode it into a **JWT** Token

method 2 and 3 can be convienent to use in case of an untrusted environment such a chatbot  
with the *gettoken* method you prepare the token with all the data encoded  
with the *ddosornotddos* method push that token in case of ddos 
