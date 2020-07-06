import logging
import socket
import threading

logging.basicConfig(level=logging.INFO)


def request_handler(conn: socket.socket):
    try:
        message: str = conn.recv(1024).decode("utf-8")
        filename = message.split()[1]
        with open(filename[1:]) as f:
            body = f.read()
        http_header = "HTTP/1.1 200 OK\r\n\r\n"

        conn.sendall(http_header.encode("utf-8"))
        conn.sendall(body.encode("utf-8"))
        conn.close()
    except IOError:
        http_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn.sendall(http_header.encode("utf-8"))
        conn.sendall("404 Not Found".encode("utf-8"))
        conn.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 5678))
server_socket.listen(5)
logging.info("Ready to serve...")


while True:
    # Establish the connection
    try:
        connection_socket, address = server_socket.accept()
        thread = threading.Thread(
            target=request_handler, args=(connection_socket,), daemon=True
        )
        thread.start()
    except (KeyboardInterrupt, OSError):
        server_socket.close()
