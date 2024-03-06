import psutil
import requests
from getmac import get_mac_address
from datetime import datetime


def get_mac_address1():
    """Retrieves the device's MAC address."""
    mac = get_mac_address()
    return mac


def collect_system_info():
    """Collects and formats system information."""
    system_info = {}

    # CPU Information
    cpu_info = {}
    cpu_info['cpu_utilization'] = psutil.cpu_percent(interval=1)
    cpu_info['cpu_cores'] = psutil.cpu_count()
    system_info["cpu"] = cpu_info

    # Memory Information
    mem_info = {}
    mem = psutil.virtual_memory()
    mem_info['total'] = mem.total / (1024 ** 3)  # Convert to GB
    mem_info['available'] = mem.available / (1024 ** 3)  # Convert to GB
    mem_info['percent'] = mem.percent
    system_info["memory"] = mem_info

    # Disk Information
    disk_info = {}
    disk = psutil.disk_usage('/')
    disk_info['total'] = disk.total / (1024 ** 3)  # Convert to GB
    disk_info['used'] = disk.used / (1024 ** 3)  # Convert to GB
    disk_info['free'] = disk.free / (1024 ** 3)  # Convert to GB
    disk_info['percent'] = disk.percent
    system_info["disk"] = disk_info

    # Network Information
    net_info = {}
    net = psutil.net_io_counters()
    net_info['bytes_sent'] = net.bytes_sent
    net_info['bytes_recv'] = net.bytes_recv
    system_info["network"] = net_info

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the datetime object
    formatted_datetime = current_datetime.isoformat()

    system_info["mac_address"] = get_mac_address1()
    system_info["time_stamp"] = formatted_datetime

    return system_info

def send_system_info(system_info, backend_url):
    try:
        response = requests.post(backend_url, json=system_info)
        response.raise_for_status()
        print("System information sent successfully!")
    except Exception as e:
        print(f"Failed to send system information: {e}")

if __name__ == "__main__":
    backend_url = "http://localhost:4000/receive_data"
    system_info = collect_system_info()
    # send_system_info(system_info, backend_url)
    print(system_info) 