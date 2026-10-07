import subprocess
import logging
from datetime import datetime

logging.basicConfig(filename='netrecon.log', level=logging.INFO)


def log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"[{now}] {msg}")


def detect_service(ip, ports):
    ports_str = ','.join(str(p) for p in ports)
    cmd = ["nmap", "-sV", "-p", ports_str, ip]
    log(f"Running service detection on {ip}:{ports_str}")
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
        log(result)
        return result
    except FileNotFoundError:
        return "Error: nmap not found. Install nmap first."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"
