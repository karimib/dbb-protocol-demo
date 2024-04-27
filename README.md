# DBB-Protocol Demo

This is a simple demo of the Hancke&Kuhn DBB-Protocol implemented as part of the "Data Security & Privacy" Course

# Single-Machine Usage

To run the demo on a single machine, follow the steps below:

1. Set the IP address of the prover in the [prover.py](./prover.py) & [verifier.py](./verifier.py) script to "localhost"
2. Run the prover.py script

```bash
python3 prover.py
```

3. Run the verifier.py script

```bash
python3 verifier.py
```

4. Follow the instructions in the terminal of the verifier script.

# Prover Machine & Verifier Machine Usage

To run the demo on two different machines, follow the steps below:

1. Set the IP address of the prover in the [prover.py](./prover.py) & [verifier.py](./verifier.py) script to the IP
   address of the prover
2. Run the prover.py script on the prover machine

```bash
python3 prover.py
```

3. Run the verifier.py script on the verifier machine

```bash
python3 verifier.py
```

4. Follow the instructions in the terminal of the verifier script.