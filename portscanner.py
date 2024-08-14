## project code
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Function to scan a specific port
def scan_port(ip, port, open_ports, lock):

    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)  # Timeout for the connection
    result = scanner.connect_ex((ip, port))
    
    if result == 0:
        with lock:
            open_ports.append(port)  # Collect open ports
    scanner.close()

# Function to start the port scan
def scan_ports(ip, port_count):

    print(f"Starting scan on host: {ip}")
    open_ports = []  # List to collect open ports
    lock = threading.Lock()  # Lock to synchronize access to open_ports
    
    # Using a ThreadPoolExecutor to limit the number of concurrent threads
    max_threads = 1000  # Limit to 1000 threads at a time (adjustable)
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in range(1, port_count + 1):
            executor.submit(scan_port, ip, port, open_ports, lock)

            # Print countdown every 100 ports
            if port % 100 == 0 or port == port_count:
                print(f"Scanning... {port}/{port_count} ports completed")
                time.sleep(0.01)  # Small sleep to prevent overwhelming the console
    
    # Wait for all threads to complete
    executor.shutdown(wait=True)
    
    # Print summary
    print(f"\nScan complete. Total open ports found: {len(open_ports)}")
    for port in open_ports:
        print(f"{port}/tcp open")

# Main function
if __name__ == "__main__":

    target = input("Enter the target domain name or IP address: ")
    try:
        # Resolve the domain name to an IP address
        target_ip = socket.gethostbyname(target)
        print(f"Resolved {target} to {target_ip}")
        
        # Ask the user for the number of ports to scan
        port_count = int(input("Enter the number of ports you want to scan (1-65535): "))
        if 1 <= port_count <= 65535:
            scan_ports(target_ip, port_count)
        else:
            print("Please enter a valid number between 1 and 65535.")
    
    except socket.gaierror:
        print(f"Error: Could not resolve domain name {target}. Please check the domain and try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")
