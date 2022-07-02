import requests
import os

PRIVATE_KEY = "<your_nordvpn_private_key>"
DNS = "8.8.8.8"

try:
    os.mkdir("configs")
except Exception:
    pass

servers = requests.get("https://api.nordvpn.com/v1/servers?limit=10000").json()

for server in servers:
    if any(technology["identifier"] == "wireguard_udp" for technology in server["technologies"]):
        address = server["hostname"]
        name = server["hostname"].split(".nordvpn.com")[0]
        for tech in server["technologies"]:
            if tech["identifier"] == "wireguard_udp":
                for meta in tech['metadata']:
                    if meta["name"] == "public_key":
                        public_key = meta['value']

        city = server["locations"][0]["country"]["city"]["name"].replace(' ', '_')

        config_content = f"""[Interface]
PrivateKey = {PRIVATE_KEY}
Address = 10.5.0.2/32
DNS = {DNS}

[Peer]
PublicKey = {public_key}
AllowedIPs = 0.0.0.0/0
Endpoint = {address}:51820
"""
        file = open(f"configs/{city}-{name}.conf", "w")
        file.write(config_content)
        file.close()
    






