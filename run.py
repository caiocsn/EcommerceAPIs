import subprocess
import psutil
import threading
import time

# Function to start a server as a subprocess
def start_server(command):
    subprocess.Popen(command, shell=True)

# Function to stop a server using its process ID
def stop_server(pid):
    process = psutil.Process(pid)
    process.terminate()

# List of commands to start the servers
inventory_api_command = "uvicorn InventoryAPI.main:app --port 8000 --reload"
orders_api_command = "uvicorn OrdersAPI.main:app --port 8001 --reload"

# Start the servers in separate threads
inventory_thread = threading.Thread(target=start_server, args=(inventory_api_command,))
orders_thread = threading.Thread(target=start_server, args=(orders_api_command,))
inventory_thread.start()
orders_thread.start()

# Sleep to allow the servers to start
time.sleep(10)

# Get the process IDs of the servers
inventory_api_pid = psutil.Process().children(recursive=True)[0].pid
orders_api_pid = psutil.Process().children(recursive=True)[1].pid

try:
    # Wait for the main code to be interrupted
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop the servers when the main code is interrupted
    stop_server(inventory_api_pid)
    stop_server(orders_api_pid)
    inventory_thread.join()
    orders_thread.join()
