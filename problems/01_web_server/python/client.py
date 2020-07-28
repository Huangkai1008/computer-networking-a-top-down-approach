import logging
import socket

import typer

logging.basicConfig(level=logging.INFO)


def create_client(host: str, port: int, filename: str):
    typer.echo(f'Client request {host}:{port}/{filename}...')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.sendall(f'Get {filename} HTTP/1.1\r\nHOST: {host}\r\n\r\n'.encode('utf-8'))
    logging.info(client.recv(1024).decode('utf-8'))


if __name__ == '__main__':
    typer.run(create_client)
