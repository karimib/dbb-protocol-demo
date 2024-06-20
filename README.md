# DBB-Protocol Demo

This implementation of Hancke&Kuhn DBP-Protocol was produced as part of the "Secure & Private Computing" Course

## Single-Host Usage

To run the demo on a single host, follow the steps below:

1. Set the IP address of the prover in the [prover.py](./prover.py) & [verifier.py](./verifier.py) script to "127.0.0.1"
2. Run the prover.py script

```bash
python3 prover.py
```

3. Run the verifier.py script

```bash
python3 verifier.py
```

4. Follow the instructions in the terminal of the verifier script.

## Prover & Verifier on different hosts (IP)

To run the demo on two different machines, follow the steps below:

1. Set the IP address in the [prover.py](./prover.py) & [verifier.py](./verifier.py) script to the private IP
   address of the machine running the prover 
2. Run the prover.py script on the prover machine

```bash
python3 prover.py
```

3. Run the verifier.py script on the verifier machine

```bash
python3 verifier.py
```

4. Follow the instructions in the terminal of the machine running the verifier script.

##  Prover & Verifier on different hosts (BT)
The following scripts establish a connection over bluetooth.
The scripts have been tested on Debian GNU/Linux 12 (bookworm).
Security Note: Be careful when using bluetooth as it posses a security risk.
In order to run the scripts bluetoothctl must be installed and the bluetooth device must be discoverable and pairable.
To get the MAC address of the bluetooth device run the following command:
```bash
hciconfig
```

1. Set the MAC address in the [prover-bt.py](./prover-bt.py) & [verifier-bt.py](./verifier-bt.py) script to the MAC
   address of the machine running the prover .
2. Run the prover-bt.py script on the prover machine

```bash
python3 prover-bt.py
```

3. Run the verifier-bt.py script on the verifier machine

```bash
python3 verifier-bt.py
```


