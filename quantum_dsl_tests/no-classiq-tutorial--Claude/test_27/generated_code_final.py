from classiq import *

@qfunc
def predicate_oracle(a: QNum, b: QNum, c: QNum, target: QBit):
    """
    Evaluates ((a + b) + (c & 6)) % 4) | (4 & c)) == 4
    """
    # Calculate the expression step by step
    sum_ab = a + b
    c_and_6 = c & 6
    total_sum = sum_ab + c_and_6
    mod_result = total_sum % 4
    four_and_c = 4 & c
    final_result = mod_result | four_and_c
    
    # Flip target if result equals 4
    target ^= (final_result == 4)

@qfunc
def phase_oracle(a: QNum, b: QNum, c: QNum):
    """Phase oracle for Grover's algorithm"""
    aux = QBit()
    within_apply(
        lambda: [allocate(1, aux), H(aux)],
        lambda: predicate_oracle(a, b, c, aux)
    )

@qfunc
def diffuser(a: QNum, b: QNum, c: QNum):
    """Grover diffusion operator"""
    # Apply H to go to computational basis
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Apply phase flip to |000> state using auxiliary qubit
    aux = QBit()
    within_apply(
        lambda: allocate(1, aux),
        lambda: control(a == 0, lambda: control(b == 0, lambda: control(c == 0, lambda: Z(aux))))
    )
    
    # Apply H to go back to superposition basis
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)

@qfunc
def grover_search(a: QNum, b: QNum, c: QNum):
    """Grover's algorithm with 3 iterations"""
    # Initialize uniform superposition
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Apply 3 Grover iterations
    for i in range(3):
        phase_oracle(a, b, c)
        diffuser(a, b, c)

@qfunc
def main(a: Output[QNum], b: Output[QNum], c: Output[QNum]):
    allocate(2, a)
    allocate(2, b)
    allocate(3, c)
    grover_search(a, b, c)

if __name__ == "__main__":
    qmod = create_model(main)
    qprog = synthesize(qmod)
    
    job = execute(qprog)
    results = job.result()[0].value
    
    print("Grover Search Results:")
    print("Searching for solutions to: ((a + b) + (c & 6)) % 4) | (4 & c)) == 4")
    print()
    
    # Parse results from parsed_states
    valid_solutions = []
    total_measurements = sum(results.counts.values())
    
    print("Top results (sorted by count):")
    # Sort by count (descending)
    sorted_states = sorted(results.parsed_states.items(), 
                          key=lambda x: results.counts[x[0]], reverse=True)
    
    for i, (bit_string, state) in enumerate(sorted_states[:20]):
        a_val = state['a']
        b_val = state['b']
        c_val = state['c']
        count = results.counts[bit_string]
        probability = count / total_measurements
        
        # Verify the predicate
        expression_result = ((a_val + b_val) + (c_val & 6)) % 4
        final_result = expression_result | (4 & c_val)
        
        is_solution = final_result == 4
        if is_solution:
            valid_solutions.append((a_val, b_val, c_val))
        
        status = "✓" if is_solution else "✗"
        print(f"{i+1:2d}. a={a_val}, b={b_val}, c={c_val}: result={final_result} {status} "
              f"(count: {count}, prob: {probability:.3f})")
    
    print(f"\nFound {len(valid_solutions)} valid solutions in top 20 results:")
    for a_val, b_val, c_val in valid_solutions:
        print(f"  ✓ a={a_val}, b={b_val}, c={c_val}")
    
    # Verify all solutions mathematically
    print(f"\nMathematical verification of all possible solutions (a∈[0,3], b∈[0,3], c∈[0,7]):")
    all_solutions = []
    for a in range(4):
        for b in range(4):
            for c in range(8):
                result = ((a + b) + (c & 6)) % 4
                final = result | (4 & c)
                if final == 4:
                    all_solutions.append((a, b, c))
    
    print(f"Total theoretical solutions: {len(all_solutions)}")
    print("All valid solutions:")
    for a, b, c in all_solutions:
        print(f"  a={a}, b={b}, c={c}")
    
    print(f"\nGrover's algorithm should amplify these {len(all_solutions)} solutions out of {4*4*8} = 128 total states.")