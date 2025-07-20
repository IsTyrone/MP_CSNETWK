import socket
import os

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 65535
FILE_DIR = "server_files"

os.makedirs(FILE_DIR, exist_ok=True)

def handle_upload(data, client_addr, server_sock):
    filename = data.decode().strip()
    server_sock.sendto(b"READY", client_addr)
    file_data, _ = server_sock.recvfrom(BUFFER_SIZE)
    with open(os.path.join(FILE_DIR, filename), "wb") as f:
        f.write(file_data)
    server_sock.sendto(b"UPLOAD_SUCCESS", client_addr)
    print(f"[SERVER] Uploaded: {filename}")

def handle_download(data, client_addr, server_sock):
    filename = data.decode().strip()
    filepath = os.path.join(FILE_DIR, filename)
    print(f"[SERVER] Attempting download: {filepath}")
    if os.path.exists(filepath):
        server_sock.sendto(b"FOUND", client_addr)
        with open(filepath, "rb") as f:
            server_sock.sendto(f.read(), client_addr)
    else:
        server_sock.sendto(b"FILE_NOT_FOUND", client_addr)

def handle_list(client_addr, server_sock):
    files = os.listdir(FILE_DIR)
    listing = "\n".join(f for f in files if os.path.isfile(os.path.join(FILE_DIR, f)))
    server_sock.sendto(listing.encode(), client_addr)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"[SERVER] Running on {SERVER_IP}:{SERVER_PORT}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        command = data.decode().strip()

        if command.startswith("UPLOAD "):
            handle_upload(command[7:].encode(), addr, sock)
        elif command.startswith("DOWNLOAD "):
            handle_download(command[9:].encode(), addr, sock)
        elif command == "LIST":
            handle_list(addr, sock)

if __name__ == "__main__":
    main()
