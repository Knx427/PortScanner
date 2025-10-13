# Simple Port Scanner Script with Python

# Libraries
# Async exec Functions -> Async Thread exec
from concurrent.futures import ThreadPoolExecutor  
# Sockets - TCP Connection
import socket
# Time - Time needed to run
import time

# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def color_text(message):
    if "Error" in message:
        return f"{RED}{message}{RESET}"
    elif "[!]" in message:
        return f"{GREEN}{message}{RESET}"
    elif "[~]" in message:
        return f"{YELLOW}{message}{RESET}"
    elif "Total Ports" in message:
        return f"{BLUE}{message}{RESET}"
    else:
        return message

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
    
    # Scan ip address in Port range per thread
def scan(ip_address, port_chunk):
    for port in range(int(port_chunk[0]), int(port_chunk[1])): # for each port range do:
        try: 
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Attempt ipv4 Connection with TCP, Sock_drgram for UDP
            scan_socket.settimeout(2) # timeout after 2 sec for next port
            
            scan_socket.connect((ip_address, port)) # Connecting to Port, if open print the port 
            print(color_text(f"[!] Port {port} is Open"))
        except: 
            None

    # user input for ip + validation
def get_valid_ip(default='192.168.1.1'):
    while True:
        ip = input(f"Enter Valid IP or hostname to Scan, (default {default}):").strip() or default 
        try:
            ip_addr = socket.gethostbyname(ip) # get ip by hostname
            print(color_text(f"[~] Using IP: {ip_addr}"))
            return ip_addr
        except socket.gaierror as e:
            print(color_text(f"Error: could not resolve '{ip or socket.gethostname()}': {e}")) # shows resolution errors

    # user input for ports + validation
def get_valid_port_range(default='0-10000'):
    while True:
        port = input(f"Enter Valid Port Range, format: start-end (default {default}):").strip() or default
        try:
            start, end = port.split('-')
            start = int(start); end = int(end)
            if 0 <= start <= end <= 65535:
                print(color_text(f"[~] Selected Ports: {start}-{end}"))
                return f"{start}-{end}"
        except Exception:
            pass
        print(color_text(f"Error: Invalid Range. Use format start-end, range: 0-65535."))

    # user input for Thread level            
def get_workers(default=100):
    choices = {"1": default, "2": 200, "3": 300, "4": 400, "5": 500, "custom" : None}
    while True:
        lvl = input(f"Enter Threads Level 1-5 (default 1={default}): ").strip() or "1"
        if lvl in choices:
            if lvl == "custom":
                while True:
                    try:
                        custom = int(input("Enter Custom Threads: ").strip())
                        if custom > 0:    
                            print(color_text(f"[~] Using Threads: {custom}\n"))                       
                            return custom
                        else:
                            print(color_text("Error: Thread count must be greater than 0."))
                    except ValueError:
                        print(color_text("Error: Please enter a valid number."))
            else:
                print(color_text(f"[~] Using Threads: {choices[lvl]}\n")) 
                return choices[lvl]
        print(color_text("Error: Invalid level. Range: 1-5."))


# main func
def main():
    ip_address = get_valid_ip() # ip address to scan
    port_range = get_valid_port_range() # port range to scan
    WORKERS = get_workers() 
    
    ports_scanned = port_range.split('-')
    port_chunks = gen_port_chunks(port_range)   # call in the port ranges 
    start_time = time.time() # start timer
    print(color_text(f"[~] Scanning {ip_address} from Port {ports_scanned[0]} to {ports_scanned[1]} using {WORKERS} threads"))
    
    with ThreadPoolExecutor(max_workers=WORKERS) as executor: # submit task to threads pool 
       executor.map(scan, [ip_address] * len(port_chunks), port_chunks) # Scan ip in port range
    
    end_time = time.time() # stop timer
    total_time = end_time - start_time
    print(f"Scanned {ports_scanned[1]} ports in \033[31m{total_time:.3f} seconds\033[0m") # calculate time elapsed

        
if __name__ == '__main__':
    main()