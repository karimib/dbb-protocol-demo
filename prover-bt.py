import random
import os
import socket

MAC = "XX:XX:XX:XX:XX:XX"
PORT = 4

SECRET_KEY = b'supersecretkey'
ITERATIONS = 10

def main():
    server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server_socket.bind((MAC, PORT))
    server_socket.listen(1)
    print(f"Listening on {MAC}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    print("=====================================")
    print("⚙️ Start: SETUP PHASE")
    verifier_nonce = conn.recv(128)
    print("📥 Received nonce N_v: ", verifier_nonce)
    prover_nonce = os.urandom(16)
    conn.sendall(prover_nonce)
    print("📥 Sent nonce: N_p: ", prover_nonce)
    random.seed(SECRET_KEY + verifier_nonce + prover_nonce)
    shared_bits = ''.join(str(random.randint(0, 1)) for _ in range(2 * ITERATIONS))
    print("📦 Shared bits b_n:", shared_bits)
    print("⚙️ End: SETUP PHASE")
    print("=====================================")

    try:
        for i in range(ITERATIONS):
            data = conn.recv(1)

            c_i = int(data.decode())
            # print("Received challenge:", challenge)
            r_i = shared_bits[(2 * i + c_i - 1)]
            # print("Generated response:", r_i)
            conn.send(str(r_i).encode())

    finally:
        conn.close()
        server_socket.close()


if __name__ == "__main__":
    main()
