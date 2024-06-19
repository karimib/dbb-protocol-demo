import random
import socket
import os
import time
import csv

SECRET_KEY = b'supersecretkey'
ITERATIONS = 10
DISTANCE_THRESHOLD = 40000
SPEED_OF_LIGHT = 299792458
MAC = "XX:XX:XX:XX:XX:XX"
PORT = 4


def main():

    client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client_socket.connect((MAC, PORT))

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
    received_responses = []
    expected_responses = []
    time_deltas = []
    try:
        for i in range(ITERATIONS):
            c_i = random.randint(0, 1)
            msg = str(c_i).encode()

            start_time = time.process_time_ns()
            client_socket.send(msg)
            data = client_socket.recv(1)
            end_time = time.process_time_ns()

            expected_responses.append(int(shared_bits[(2 * i + c_i - 1)]))
            received_responses.append(int(data.decode()))
            time_deltas.append(end_time - start_time)

        print("=====================================")
        print("🏁End: CHALLENGE PHASE")
        print("⚙️ Start: VERIFICATION PHASE")
        valid_responses = 0
        valid_distance = 0
        for i in range(ITERATIONS):
            valid_responses += 1 if expected_responses[i] == received_responses[i] else 0
            valid_distance += 1 if time_deltas[i] < 2 * DISTANCE_THRESHOLD else 0

        avg_rtt = sum(time_deltas) / len(time_deltas)
        print("📊 Valid responses:", valid_responses)
        print("📊 Valid distance:", valid_distance)
        print("📊 Average round trip time (ns):", avg_rtt)
        print("📊 Average distance (m):", avg_rtt * SPEED_OF_LIGHT)

        with open('output-bt.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            # Write each row in the list to the file
            for row in time_deltas:
                writer.writerow([row])

    finally:
            client_socket.close()

    print("=====================================")
    print("🏁End: CHALLENGE PHASE")


if __name__ == "__main__":
    main()
