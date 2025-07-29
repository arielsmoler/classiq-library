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
    for state, count in results.parsed_counts.items():
        a_val = state['a']
        b_val = state['b']
        c_val = state['c']
        
        # Verify the predicate
        result = ((a_val + b_val) + (c_val & 6)) % 4
        final = result | (4 & c_val)
        
        print(f"a={a_val}, b={b_val}, c={c_val}: result={final} {'✓' if final == 4 else '✗'} (count: {count})")