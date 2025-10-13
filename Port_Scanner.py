# Simple Port Scanner Script with Python

# Libraries
# Async exec Functions -> Async Thread exec
from concurrent.futures import ThreadPoolExecutor  
# Sockets - TCP Connection
import socket
# Time - Time needed to run
import time

WORKERS = 100 # Threads to use

    # Gen Port ranges to scan
def gen_port_chunks(port_range):
    port_ranges = port_range.split('-') # [0-100]...
    port_chunks = [] # store the splited ports in array
    chunk_size = int((int(port_ranges[1]) - int(port_ranges[0])) / WORKERS) # get ports range per worker
    
    # split ports to worker amount
    for i in range(WORKERS):
        start = int(port_ranges[0]) + (chunk_size * i) 
        end = start + chunk_size
        port_chunks.append([start, end])
    return port_chunks # return splited port ranges
    
    # Scan ip address in Port range 
def scan(ip_address, port_chunk):
    print(f"[~] Scanning {ip_address} from {port_chunk[0]} to {port_chunk[1]}.") # eg. Scan 192.169.1.1 from 0 to 100
    for port in range(int(port_chunk[0]), int(port_chunk[1])): # for each port range do:
        try: 
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Attempt ipv4 Connection with TCP, Sock_drgram for UDP
            scan_socket.settimeout(2) # timeout after 2 sec for next port
            
            scan_socket.connect((ip_address, port)) # Connecting to Port, if open print the port 
            print(f"[!] Port {port} is Open")
        except: 
            None

    # user input for ip + validation
def get_valid_ip(default='192.168.1.1'):
    while True:
        ip = input(f"Enter Valid IP or hostname to Scan, (default {default}):").strip() or default 
        try:
            ip_addr = socket.gethostbyname(ip) # get ip by hostname
            if ip_addr == socket.gethostbyname(socket.gethostname()):
                print(f"Using local ip: {ip_addr}")
            else:
                print(f"Using IP: {ip_addr}")
            return ip_addr
        except socket.gaierror as e:
            print(f"Error: could not resolve '{ip or socket.gethostname()}': {e}") # shows resolution errors

    # user input for ports + validation
def get_valid_port_range(default='0-10000'):
    while True:
        port = input(f"Enter Valid Port Range, format: start-end (default {default}):").strip() or default
        try:
            start, end = port.split('-')
            start = int(start); end = int(end)
            if 0<=start <= end <= 65535:
                return f"{start}-{end}"
        except Exception:
            pass
        print(f"Invalid Range. Use format start-end, range: 0-65535.")

    # user input for Thread level            
def get_workers(default=100):
    choices = {"1": default, "2": 200, "3": 300, "4": 400, "5": 500}
    while True:
        lvl = input(f"Enter Threads Level 1-5 (default 1={default}): ").strip() or "1"
        if lvl in choices:
            return choices[lvl]
        print("Invalid level. Range: 1-5.")


# main func
def main():
    ip_address = get_valid_ip() # ip address to scan
    port_range = get_valid_port_range() # port range to scan
    WORKERS = get_workers() 
    
    port_chunks = gen_port_chunks(port_range)   # call in the port ranges 
    start_time = time.time() # start timer
    with ThreadPoolExecutor(max_workers=WORKERS) as executor: # submit task to threads pool 
        executor.map(scan, [ip_address] * len(port_chunks), port_chunks) # Scan ip in port range
    end_time = time.time() # stop timer
    print(f"Scanned {port_range[1]} ports in {end_time - start_time} seconds.") # calculate time elapsed
    print(f"Used {WORKERS} threads") # Show thread level used

        
if __name__ == '__main__':
    main()