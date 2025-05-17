import requests
import subprocess
import re

def get_game_prefixes(asn: str) -> list:
    url = f"https://api.bgpview.io/asn/{asn}/prefixes"
    try:
        res = requests.get(url)
        data = res.json()
        return [p['prefix'] for p in data['data']['ipv4_prefixes']]
    except Exception as e:
        print("Failed to fetch:", e)
        return []

def list_interfaces() -> list:
    output = subprocess.check_output(
        "netsh interface ip show config", shell=True, text=True
    )

    interfaces = []
    current_iface = None
    gateway = None

    for line in output.splitlines():
        line = line.strip()

        # detect the start of a new interface block
        if line.startswith("Configuration for interface"):               
            current_iface = re.search(r'"(.+?)"', line).group(1)

        # detect the end of an interface block (for us, since we need only the IF name and gateway)
        elif line.startswith("Default Gateway:"):
            match = re.search(r"Default Gateway:\s+([\d.]+)", line)
            if match:
                gateway = match.group(1)
                print(current_iface, gateway)
                interfaces.append({
                    "name": current_iface,
                    "gateway": gateway
                })
            
            # reset values
            current_iface = None
            gateway = None

    return interfaces

def apply_routes(prefixes: list, gateway: str) -> bool:
    for prefix in prefixes:
        try:
            subprocess.run(['route', 'add', prefix, gateway], check=True)
        except Exception as e:
            print(f"Failed to add route for {prefix}: {e}")
            return False
    return True

