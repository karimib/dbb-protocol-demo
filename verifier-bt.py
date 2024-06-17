import random
import socket
import os
import time

SECRET_KEY = b'supersecretkey'
ITERATIONS = 10
DISTANCE_THRESHOLD = 40000
SPEED_OF_LIGHT = 299792458
MAC = "XX:XX:XX:XX:XX:XX"


def main():

    client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client_socket.connect(MAC)

    input("Press Enter to start: SETUP PHASE")
    print("=====================================")
    print("⚙️ Start: SETUP PHASE")
    verifier_nonce = os.urandom(16)
    client_socket.sendall(verifier_nonce)
    print("📥 Sent nonce N_v: ", verifier_nonce)
    prover_nonce = client_socket.recv(128)
    print("📤 Received nonce N_p: ", prover_nonce)
    random.seed(SECRET_KEY + verifier_nonce + prover_nonce)
    shared_bits = ''.join(str(random.randint(0, 1)) for _ in range(2 * ITERATIONS))
    print("📦 Shared bits b_n:", shared_bits)
    print("🏁 End: SETUP PHASE")
    print("=====================================")

    input("Press Enter to start: CHALLENGE PHASE")
    print("=====================================")
    print("⚙️ Start: CHALLENGE PHASE")

    try:
        for i in range(ITERATIONS):
            print("=====================================")
            print("🚩ITERATION: ", i)
            c_i = random.randint(0, 1)
            print(">Sending challenge:", c_i)
            msg = str(c_i).encode()

            start_time = time.perf_counter_ns()
            client_socket.send(msg)
            data = client_socket.recv(1)
            end_time = time.perf_counter_ns()

            expected_response = shared_bits[(2 * i + c_i - 1)]
            response = str(int(data.decode()))
            print("<Received response:", response)
            print("=Expected response:", expected_response)

            if expected_response == response:
                print("✅ Valid response received")
            else:
                print("❌ Invalid response or tampering detected")

            round_trip_time = (end_time - start_time) / 1e9
            distance = ((round_trip_time / 2) * SPEED_OF_LIGHT)
            print("=Round trip time:", round_trip_time, "s")
            print("=Distance: ", distance, "meters")
            if distance < DISTANCE_THRESHOLD:
                print("✅RESULT: Prover is within threshold")
            else:
                print("❌RESULT: Prover is outside threshold")


    finally:
        client_socket.close()

    print("=====================================")
    print("🏁End: CHALLENGE PHASE")


if __name__ == "__main__":
    main()
