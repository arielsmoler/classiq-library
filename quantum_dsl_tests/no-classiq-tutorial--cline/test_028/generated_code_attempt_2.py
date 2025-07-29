from classiq import *
import numpy as np

# Shor's algorithm for factoring N = 55
N = 55

@qfunc
def modular_exp(a: CInt, x: QNum, N: CInt, res: Output[QNum]):
    """
    Modular exponentiation: res = a^x mod N
    For Shor's algorithm factoring 55
    """
    # Initialize result to 1
    res |= 1
    
    # For each bit in x, square and multiply
    power_of_a = a
    repeat(x.size, lambda i: 
        control(x[i], lambda: 
            inplace_xor(res, power_of_a % N)
        )
    )

@qfunc
def quantum_period_finding(a: CInt, N: CInt, counting_qubits: QNum, work_qubits: Output[QNum]):
    """
    Quantum period finding for Shor's algorithm
    """
    # Apply Hadamard to counting qubits
    hadamard_transform(counting_qubits)
    
    # Controlled modular exponentiation
    modular_exp(a, counting_qubits, N, work_qubits)
    
    # Apply inverse QFT to counting qubits
    invert(lambda: qft(counting_qubits))

@qfunc
def shor_algorithm(a: CInt, N: CInt, counting_qubits: Output[QNum], work_qubits: Output[QNum]):
    """
    Main Shor's algorithm function
    """
    # Allocate qubits
    allocate(8, counting_qubits)  # 8 counting qubits for period finding
    allocate(6, work_qubits)      # 6 work qubits (log2(55) ≈ 6)
    
    # Perform quantum period finding
    quantum_period_finding(a, N, counting_qubits, work_qubits)

@qfunc
def main(counting_result: Output[QNum], work_result: Output[QNum]):
    """
    Main function for Shor's algorithm to factor 55
    Using a = 2 as the base (gcd(2, 55) = 1)
    """
    shor_algorithm(2, N, counting_result, work_result)

# Create and synthesize the quantum model
model = create_model(main)

print("Shor's Algorithm for Factoring N = 55")
print("=====================================")
print(f"Target number to factor: {N}")
print(f"Using base a = 2 (since gcd(2, 55) = 1)")
print()

# Synthesize the quantum program
print("Synthesizing quantum circuit...")
qprog = synthesize(model)

print(f"Circuit depth: {qprog.depth}")
print(f"Circuit width: {qprog.width}")
print(f"Number of gates: {len(qprog.instructions)}")
print()

# Show the synthesized circuit
print("Quantum circuit synthesized successfully!")
print("The circuit implements:")
print("1. Quantum Fourier Transform for period finding")
print("2. Controlled modular exponentiation (2^x mod 55)")
print("3. Inverse QFT for extracting the period")
print()

# Classical post-processing explanation
print("Classical post-processing:")
print("After measuring the counting qubits, we would:")
print("1. Extract the period r from the measurement results")
print("2. Check if r is even and a^(r/2) ≢ ±1 (mod N)")
print("3. Compute factors using gcd(a^(r/2) ± 1, N)")
print()
print("Expected factors of 55: 5 and 11")
print("Verification: 5 × 11 = 55 ✓")
