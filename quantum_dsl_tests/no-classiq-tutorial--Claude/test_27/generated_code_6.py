from classiq import *

@qfunc
def predicate_oracle(a: QNum, b: QNum, c: QNum, target: QBit):
    """
    Evaluates ((a + b) + (c & 6)) % 4) | (4 & c)) == 4
    """
    # Calculate a + b
    sum_ab = a + b
    
    # Calculate c & 6
    c_and_6 = c & 6
    
    # Calculate (a+b) + (c&6)
    total_sum = sum_ab + c_and_6
    
    # Calculate mod 4
    mod_result = total_sum % 4
    
    # Calculate 4 & c  
    four_and_c = 4 & c
    
    # Final OR operation
    final_result = mod_result | four_and_c
    
    # Flip target if result equals 4
    target ^= (final_result == 4)

@qfunc
def phase_oracle(a: QNum, b: QNum, c: QNum):
    """Phase oracle - flips phase for states satisfying predicate"""
    aux = QBit("aux")
    within_apply(
        compute=lambda: [allocate(1, aux), H(aux)],
        action=lambda: predicate_oracle(a, b, c, aux)
    )

@qfunc  
def diffuser(a: QNum, b: QNum, c: QNum):
    """Grover diffusion operator"""
    # Apply Hadamard gates
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Flip phase of |000> state
    aux = QBit("aux")
    within_apply(
        compute=lambda: allocate(1, aux),
        action=lambda: control(a == 0, lambda: control(b == 0, lambda: control(c == 0, lambda: X(aux))))
    )
    
    # Apply Hadamard gates again
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)

@qfunc
def grover_iteration(a: QNum, b: QNum, c: QNum):
    """Single Grover iteration"""
    phase_oracle(a, b, c)
    diffuser(a, b, c)

@qfunc
def grover_search(a: QNum, b: QNum, c: QNum):
    """Grover's search with 3 iterations"""
    # Initialize superposition
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Run 3 Grover iterations
    grover_iteration(a, b, c)
    grover_iteration(a, b, c)
    grover_iteration(a, b, c)

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
    print("Solutions for ((a + b) + (c & 6)) % 4) | (4 & c)) == 4:")
    
    for state, count in results.parsed_counts.items():
        a_val = state['a']
        b_val = state['b']
        c_val = state['c']
        
        # Verify predicate
        result = ((a_val + b_val) + (c_val & 6)) % 4
        final = result | (4 & c_val)
        
        status = "✓" if final == 4 else "✗"
        print(f"a={a_val}, b={b_val}, c={c_val}: {final} {status} (count: {count})")