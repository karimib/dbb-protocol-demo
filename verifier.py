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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    wait = input("Press Enter to continue...")

    print("Start: Setup Phase")
    verifier_nonce = os.urandom(16)
    client_socket.sendall(verifier_nonce)
    print(">Sent nonce N_v: ", verifier_nonce)
    prover_nonce = client_socket.recv(128)
    print("<Received nonce N_p: ", prover_nonce)
    random.seed(secret_key + verifier_nonce + prover_nonce)
    shared_bits = ''.join(str(random.randint(0, 1)) for _ in range(2*iterations))
    print("Shared bits:", shared_bits)
    print("End: Setup Phase")

    try:
        for i in range(iterations):  # 10 challenge-response rounds
            c_i = random.randint(0, 1)
            print(">Sending challenge:", c_i)

            start_time = time.perf_counter_ns()
            client_socket.send(str(c_i).encode())
            data = client_socket.recv(1)
            end_time = time.perf_counter_ns()
            expected_response = shared_bits[(2 * i + c_i - 1)]
            print("<Received response:", data)
            print("Expected response:", expected_response)
            response = str(int(data.decode()))


            if expected_response == response:
                print("<Valid response received")
            else:
                print("<Invalid response or tampering detected")

            print("=Round trip time:", (end_time - start_time) / 1e6, "ms")

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
