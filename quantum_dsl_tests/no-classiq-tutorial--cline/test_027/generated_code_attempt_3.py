from classiq import *

@qfunc
def predicate_oracle(a: QNum, b: QNum, c: QNum, target: QBit):
    """
    Predicate function that evaluates: ((a + b) + (c & 6)) % 4) | (4 & c)) == 4
    """
    # Calculate a + b
    sum_ab = a + b
    
    # Calculate c & 6 (bitwise AND with 6 = 110 in binary)
    c_and_6 = c & 6
    
    # Calculate (a + b) + (c & 6)
    sum_total = sum_ab + c_and_6
    
    # Calculate ((a + b) + (c & 6)) % 4
    mod_result = sum_total % 4
    
    # Calculate 4 & c (bitwise AND with 4 = 100 in binary)
    four_and_c = 4 & c
    
    # Calculate final result: (mod_result) | (four_and_c)
    final_result = mod_result | four_and_c
    
    # Check if final_result == 4
    target ^= final_result == 4

@qfunc
def phase_oracle(a: QNum, b: QNum, c: QNum):
    """
    Phase oracle that applies a phase flip when the predicate is satisfied
    """
    aux = QBit("aux")
    within_apply(
        lambda: [H(aux), Z(aux)],
        lambda: predicate_oracle(a, b, c, aux)
    )

@qfunc
def grover_diffuser(qvars: QArray[QBit]):
    """
    Grover diffusion operator (inversion about average)
    """
    within_apply(
        lambda: apply_to_all(H, qvars),
        lambda: within_apply(
            lambda: apply_to_all(X, qvars),
            lambda: control(qvars[:-1], lambda: Z(qvars[-1]))
        )
    )

@qfunc
def grover_search(a: Output[QNum], b: Output[QNum], c: Output[QNum]):
    """
    Main Grover search function with 3 iterations
    """
    # Initialize quantum variables with proper allocation
    allocate(2, a)  # 2 qubits for a
    allocate(2, b)  # 2 qubits for b  
    allocate(3, c)  # 3 qubits for c
    
    # Create superposition of all possible states
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Apply Grover iterations (3 times)
    for _ in range(3):
        # Apply phase oracle
        phase_oracle(a, b, c)
        
        # Apply diffusion operator
        all_qubits = QArray("all_qubits")
        all_qubits |= a.qubits + b.qubits + c.qubits
        grover_diffuser(all_qubits)

@qfunc
def main(a: Output[QNum], b: Output[QNum], c: Output[QNum]):
    grover_search(a, b, c)

# Create and synthesize the quantum program
qmod = create_model(main)
qprog = synthesize(qmod)

# Execute the program
job = execute(qprog)
results = job.result()

print("Grover Search Results:")
print(f"Counts: {results[0].counts}")

# Analyze results to find solutions
print("\nAnalyzing solutions:")
for state, count in results[0].counts.items():
    if count > 0:
        # Parse the state (7 qubits total: 2 for a, 2 for b, 3 for c)
        state_bits = state
        a_val = int(state_bits[-2:], 2)  # Last 2 bits for a
        b_val = int(state_bits[-4:-2], 2)  # Next 2 bits for b  
        c_val = int(state_bits[-7:-4], 2)  # First 3 bits for c
        
        # Verify the predicate
        result = ((a_val + b_val) + (c_val & 6)) % 4
        final = result | (4 & c_val)
        
        print(f"State {state}: a={a_val}, b={b_val}, c={c_val}")
        print(f"  Calculation: (({a_val} + {b_val}) + ({c_val} & 6)) % 4 | (4 & {c_val}) = {final}")
        print(f"  Satisfies predicate (== 4): {final == 4}")
        print(f"  Count: {count}")
        print()
