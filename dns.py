import platform

def get_hosts_path():
    system = platform.system()
    if system == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif system in ("Linux", "Darwin"):  # Darwin = macOS
        return "/etc/hosts"
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

def add_dns_entry(hostname: str, ip: str = "127.0.0.1"):
    path = get_hosts_path()
    entry = f"{ip}\t{hostname}\n"

    with open(path, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        if any(hostname in line for line in lines):
            return
        f.write(entry)