import socket
import os
import hmac
import hashlib
import time


def main():
    host = 'localhost'
    port = 18080
    secret_key = b'supersecretkey'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    try:
        while True:
            data = conn.recv(128)
            if not data:
                break

            # Extract nonce and challenge
            nonce, challenge = data[:16], data[16:]
            print("Received nonce and challenge:", nonce, challenge)
            response = generate_response(challenge, secret_key)
            hmac_result = hmac.new(secret_key, nonce + challenge + response, hashlib.sha256).digest()

            # Send response and HMAC
            conn.sendall(response + hmac_result)
            print("Sent response and HMAC")

    finally:
        conn.close()
        server_socket.close()


def generate_response(challenge, secret_key):
    return bytes([challenge[i] ^ secret_key[i % len(secret_key)] for i in range(len(challenge))])


if __name__ == "__main__":
    main()
