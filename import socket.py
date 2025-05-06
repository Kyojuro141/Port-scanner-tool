import socket
import threading

# Function to scan a single port
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout of 1 second
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                # Wait a moment before trying to receive data
                sock.settimeout(2)  # Set a longer timeout for receiving data
                banner = sock.recv(1024).decode().strip()
            except socket.timeout:
                banner = 'No banner (timeout)'
            except Exception as e:
                banner = f'Error: {str(e)}'
            print(f"[+] Port {port} is open | Banner: {banner}")
        sock.close()
    except Exception as e:
        print(f"[-] Error scanning port {port}: {str(e)}")

# Main function
def port_scanner(ip, ports):
    print(f"Scanning {ip} for open ports...")
    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(ip, port))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    port_range = input("Enter port range (e.g. 1-100): ")

    start, end = map(int, port_range.split('-'))
    ports = range(start, end + 1)
    port_scanner(target_ip, ports)
