import socket
import os
import hmac
import hashlib
import time

def main():
    host = 'localhost'
    port = 18080
    secret_key = b'supersecretkey'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        for i in range(10):  # 10 challenge-response rounds
            nonce = os.urandom(16)
            challenge = os.urandom(16)
            print("Sending nonce and challenge:", nonce, challenge)
            start_time = time.perf_counter_ns()
            client_socket.sendall(nonce + challenge)

            data = client_socket.recv(128)
            end_time = time.perf_counter_ns()
            response, received_hmac = data[:len(challenge)], data[len(challenge):]
            expected_hmac = hmac.new(secret_key, nonce + challenge + response, hashlib.sha256).digest()

            if hmac.compare_digest(received_hmac, expected_hmac):
                print("Valid response received")
            else:
                print("Invalid response or tampering detected")

            print("Round trip time:", (end_time - start_time) / 1e6, "ms")

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
