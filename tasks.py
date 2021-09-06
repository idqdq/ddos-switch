from dns import tsigkeyring, update, query
from dns.tsig import HMAC_SHA256
from scrapli.driver.core import IOSXEDriver, NXOSDriver
import time

my_device = { 
    'host': '192.168.99.91',
    'auth_username': 'bot',
    'auth_password': 'Bot12345!',
    'auth_strict_key': False, 
    'ssh_config_file': True, 
}   

ZONE = 'test.arpa.'
DNS_SERV = '127.0.0.1'

def doDNSUpdate(data):    
    keyring = tsigkeyring.from_text({data.tsig_keyname: data.tsig_secret })
    IP = str(data.subst_IP) if data.ddos else str(data.prim_IP)

    upd = update.Update(ZONE, keyring=keyring, keyalgorithm=HMAC_SHA256)
    upd.replace(data.name, 300, 'A', IP)
    response = query.tcp(upd, DNS_SERV, timeout=10)
    print("DNS update done!")
    return response


def waitTTLsecs(ttl):
    time.sleep(ttl)
    print("times's up")


def blackHole(ip, ddos=True):
    with NXOSDriver(**my_device) as conn:     
        if ddos:
            cmd = f"ip route {ip} 255.255.255.255 Null0 tag 666"
        else:
            cmd = f"no ip route {ip} 255.255.255.255 Null0"

        res = conn.send_config(cmd)

        if not res.failed:            
            p = "RTHB went good" if ddos else "deativating RTHB went good"            
        else:
            p = "RTHB didn't make it" if ddos else "deactivating RTHB didn't make it"
        print(p)
    
