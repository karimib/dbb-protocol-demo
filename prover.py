import random
import socket
import os
import hmac
import hashlib
import time

secret_key = b'supersecretkey'
iterations = 10


def main():
    host = 'localhost'
    port = 18080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    print("Start: Setup Phase")
    verifier_nonce = conn.recv(128)
    print("Received nonce N_v: ", verifier_nonce)
    prover_nonce = os.urandom(16)
    conn.sendall(prover_nonce)
    print("Sent nonce: N_p: ", prover_nonce)
    random.seed(secret_key + verifier_nonce + prover_nonce)
    shared_bits = ''.join(str(random.randint(0, 1)) for _ in range(2*iterations))
    print("Shared bits:", shared_bits)
    print("End: Setup Phase")

    try:
        for i in range(iterations):
            data = conn.recv(1)
            # Extract nonce and challenge
            challenge = int(data.decode())
            print("Received challenge:", challenge)
            r_i = shared_bits[(2 * i + challenge - 1)]
            print("Generated response:", r_i)
            conn.send(str(r_i).encode())

    finally:
        conn.close()
        server_socket.close()


if __name__ == "__main__":
    main()
