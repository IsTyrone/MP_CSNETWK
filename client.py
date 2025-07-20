import socket
import os

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 65535

def upload_file(sock):
    filename = input("Enter filename to upload: ").strip()
    if not os.path.exists(filename):
        print("File not found.")
        return
    sock.sendto(f"UPLOAD {filename}".encode(), (SERVER_IP, SERVER_PORT))
    status, _ = sock.recvfrom(BUFFER_SIZE)
    if status == b"READY":
        with open(filename, "rb") as f:
            sock.sendto(f.read(), (SERVER_IP, SERVER_PORT))
        result, _ = sock.recvfrom(BUFFER_SIZE)
        print(result.decode())
    else:
        print("Server not ready.")

def download_file(sock):
    filename = input("Enter filename to download: ").strip()
    sock.sendto(f"DOWNLOAD {filename}".encode(), (SERVER_IP, SERVER_PORT))
    status, _ = sock.recvfrom(BUFFER_SIZE)
    if status == b"FOUND":
        file_data, _ = sock.recvfrom(BUFFER_SIZE)
        with open(filename, "wb") as f:
            f.write(file_data)
        print("Downloaded successfully.")
    else:
        print("File not found on server.")

def list_files(sock):
    sock.sendto(b"LIST", (SERVER_IP, SERVER_PORT))
    data, _ = sock.recvfrom(BUFFER_SIZE)
    print("Files on server:")
    print(data.decode())

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        print("\n== File Exchange Client ==")
        print("1. Upload File")
        print("2. Download File")
        print("3. List Files")
        print("4. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            upload_file(sock)
        elif choice == "2":
            download_file(sock)
        elif choice == "3":
            list_files(sock)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
