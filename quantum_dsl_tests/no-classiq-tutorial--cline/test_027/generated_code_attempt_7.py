from classiq import *

@qfunc
def oracle_function(a: QNum, b: QNum, c: QNum, target: QBit):
    """
    Oracle function that evaluates: ((a + b) + (c & 6)) % 4) | (4 & c)) == 4
    """
    # Calculate the expression step by step
    sum_ab = a + b
    c_and_6 = c & 6
    sum_total = sum_ab + c_and_6
    mod_result = sum_total % 4
    four_and_c = 4 & c
    final_result = mod_result | four_and_c
    
    # Flip target if result equals 4
    target ^= final_result == 4

@qfunc
def phase_oracle(a: QNum, b: QNum, c: QNum):
    """
    Phase oracle - applies phase flip to states satisfying the condition
    """
    aux = QBit("aux")
    allocate(1, aux)
    
    # Put auxiliary in |-> state
    X(aux)
    H(aux)
    
    # Apply oracle
    oracle_function(a, b, c, aux)
    
    # Return auxiliary to |0> state
    H(aux)
    X(aux)

@qfunc
def diffusion_operator(a: QNum, b: QNum, c: QNum):
    """
    Diffusion operator (inversion about average)
    """
    # Apply Hadamard to all qubits
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Apply X to all qubits
    invert(a)
    invert(b)
    invert(c)
    
    # Apply multi-controlled Z
    control(a.qubits + b.qubits + c.qubits[:-1], lambda: Z(c.qubits[-1]))
    
    # Apply X to all qubits
    invert(a)
    invert(b)
    invert(c)
    
    # Apply Hadamard to all qubits
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)

@qfunc
def main(a: Output[QNum], b: Output[QNum], c: Output[QNum]):
    # Allocate qubits
    allocate(2, a)  # 2 qubits for a (values 0-3)
    allocate(2, b)  # 2 qubits for b (values 0-3)
    allocate(3, c)  # 3 qubits for c (values 0-7)
    
    # Initialize in superposition
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Apply 3 Grover iterations
    # Iteration 1
    phase_oracle(a, b, c)
    diffusion_operator(a, b, c)
    
    # Iteration 2
    phase_oracle(a, b, c)
    diffusion_operator(a, b, c)
    
    # Iteration 3
    phase_oracle(a, b, c)
    diffusion_operator(a, b, c)

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
        # Assuming the bit order is c[2]c[1]c[0]b[1]b[0]a[1]a[0]
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
