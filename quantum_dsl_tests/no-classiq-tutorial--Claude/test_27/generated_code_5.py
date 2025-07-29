from classiq import *

@qfunc
def predicate_function(a: QNum, b: QNum, c: QNum, res: QBit):
    """
    Evaluates ((a + b) + (c & 6)) % 4) | (4 & c)) == 4
    """
    # First calculate a + b
    ab_sum = a + b
    
    # Calculate c & 6
    c_and_6 = c & 6
    
    # Calculate (a+b) + (c&6)
    temp_sum = ab_sum + c_and_6
    
    # Calculate mod 4
    mod_result = temp_sum % 4
    
    # Calculate 4 & c
    four_and_c = 4 & c
    
    # Final OR operation
    final_result = mod_result | four_and_c
    
    # Check if equals 4
    res ^= (final_result == 4)

@qfunc
def oracle(a: QNum, b: QNum, c: QNum):
    """Phase oracle for Grover's algorithm"""
    aux = QBit("aux")
    within_apply(
        lambda: [allocate(1, aux), H(aux)],
        lambda: predicate_function(a, b, c, aux)
    )

@qfunc
def diffusion_operator(a: QNum, b: QNum, c: QNum):
    """Grover diffusion operator"""
    # Apply Hadamard to all qubits
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Apply conditional phase flip on |0,0,0>
    control((a == 0) & (b == 0) & (c == 0), lambda: PHASE(3.14159))
    
    # Apply Hadamard to all qubits again
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)

@qfunc
def grover_search(a: QNum, b: QNum, c: QNum):
    """Grover's algorithm with 3 iterations"""
    # Initialize superposition
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Perform 3 Grover iterations
    for i in range(3):
        oracle(a, b, c)
        diffusion_operator(a, b, c)

@qfunc
def main(a: Output[QNum], b: Output[QNum], c: Output[QNum]):
    # Allocate quantum registers
    allocate(2, a)  # 2 qubits for a
    allocate(2, b)  # 2 qubits for b
    allocate(3, c)  # 3 qubits for c
    
    # Run Grover's search
    grover_search(a, b, c)

if __name__ == "__main__":
    # Create and execute the quantum program
    qmod = create_model(main)
    qprog = synthesize(qmod)
    
    job = execute(qprog)
    results = job.result()[0].value
    
    print("Grover's Search Results:")
    print("Solutions for ((a + b) + (c & 6)) % 4) | (4 & c)) == 4:")
    print()
    
    for state, probability in results.parsed_counts.items():
        a_val = state['a']
        b_val = state['b']
        c_val = state['c']
        
        # Verify the condition
        expression_result = ((a_val + b_val) + (c_val & 6)) % 4
        final_result = expression_result | (4 & c_val)
        
        is_solution = final_result == 4
        print(f"a={a_val}, b={b_val}, c={c_val}: {final_result} {'✓' if is_solution else '✗'} (prob: {probability:.3f})")
    
    print("\nVerifying solutions:")
    for state, probability in results.parsed_counts.items():
        a_val = state['a']
        b_val = state['b']
        c_val = state['c']
        
        expression_result = ((a_val + b_val) + (c_val & 6)) % 4
        final_result = expression_result | (4 & c_val)
        
        if final_result == 4:
            print(f"✓ Found valid solution: a={a_val}, b={b_val}, c={c_val}")