## **Port Scanner**

### Description

The Port Scanner is a Python script designed to scan a range of ports on a specified host and identify which ports are open. The script uses concurrent threading to efficiently scan up to 65,535 ports, providing quick results and real-time progress updates.

**Features:**
- **Scans a range of ports:** Allows users to specify the number of ports to scan, from 1 to 65,535.
- **Concurrent scanning:** Utilizes threading to scan multiple ports simultaneously for faster results.
- **Real-time progress updates:** Provides ongoing updates on the number of remaining ports during the scan.

**Intended Users:**
- **Network Administrators:** To check the availability of services and secure network configurations.
- **Security Professionals:** For assessing potential vulnerabilities by identifying open ports on target systems.
- **Developers:** To troubleshoot and ensure that necessary ports are accessible during development.


## Usage/Examples

---

## **Usage**

To use the port scanning script, follow these steps:

1. **Run the Script:**
   - Execute the script using Python from the command line or terminal.

   ```bash
   python port_scanner.py
   ```

2. **Input the Target:**
   - Enter the domain name or IP address of the target host you want to scan.

3. **Specify the Number of Ports:**
   - Enter the number of ports you want to scan. The script will scan ports starting from 1 up to the number you specify (up to 65535).

### **Example**

Here’s an example of how to use the script:

1. **Run the Script:**

   ```bash
   python port_scanner.py
   ```

2. **Input the Target:**
   - When prompted, enter a domain name or IP address, such as `example.com` or `192.168.1.1`.

   ```
   Enter the target domain name or IP address: example.com
   ```

3. **Specify the Number of Ports:**
   - Enter the number of ports you want to scan. For example, to scan the first 100 ports:

   ```
   Enter the number of ports you want to scan (1-65535): 100
   ```

4. **View Results:**
   - The script will resolve the domain name to an IP address, start scanning the specified number of ports, and print out which ports are open.

   ```
   Resolved example.com to 93.184.216.34
   Starting scan on host: 93.184.216.34
   Scanning... 100 ports remaining
   22/tcp  open
   80/tcp  open
   ...
   ```

In this example, the script will scan the first 100 ports on `example.com` and print out any open ports it finds.

---


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

