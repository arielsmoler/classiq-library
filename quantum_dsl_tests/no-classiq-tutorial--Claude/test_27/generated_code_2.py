from classiq import *
import numpy as np

@qfunc
def predicate_oracle(a: QNum, b: QNum, c: QNum, target: QBit):
    """
    Evaluates the expression ((a + b) + (c & 6)) % 4) | (4 & c)) == 4
    """
    # Calculate (a + b)
    sum_ab = QNum("sum_ab", 3, False)
    sum_ab |= a + b
    
    # Calculate (c & 6)
    c_and_6 = QNum("c_and_6", 3, False)
    c_and_6 |= c & 6
    
    # Calculate (sum_ab + c_and_6)
    sum_total = QNum("sum_total", 4, False)
    sum_total |= sum_ab + c_and_6
    
    # Calculate (sum_total % 4)
    mod_result = QNum("mod_result", 2, False)
    mod_result |= sum_total % 4
    
    # Calculate (4 & c)
    four_and_c = QNum("four_and_c", 3, False)
    four_and_c |= 4 & c
    
    # Calculate final OR operation
    final_result = QNum("final_result", 3, False)
    final_result |= mod_result | four_and_c
    
    # Check if result equals 4
    target ^= final_result == 4

@qfunc
def phase_oracle(a: QNum, b: QNum, c: QNum):
    """
    Phase oracle that flips the phase if predicate is satisfied
    """
    aux = QBit("aux")
    within_apply(
        lambda: H(aux),
        lambda: predicate_oracle(a, b, c, aux)
    )

@qfunc
def diffuser(a: QNum, b: QNum, c: QNum):
    """
    Grover diffusion operator
    """
    # Create uniform superposition state
    hadamard_transform(a)
    hadamard_transform(b) 
    hadamard_transform(c)
    
    # Apply phase flip to |0...0> state
    control(a == 0 and b == 0 and c == 0, lambda: PHASE(np.pi))
    
    # Return to superposition
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)

@qfunc
def grover_algorithm(a: QNum, b: QNum, c: QNum):
    """
    Main Grover search algorithm with 3 iterations
    """
    # Initialize superposition
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Apply Grover iterations (3 times)
    for i in range(3):
        # Apply phase oracle
        phase_oracle(a, b, c)
        
        # Apply diffuser
        diffuser(a, b, c)

@qfunc
def main(a: Output[QNum], b: Output[QNum], c: Output[QNum]):
    allocate(2, a)
    allocate(2, b)
    allocate(3, c)
    grover_algorithm(a, b, c)

if __name__ == "__main__":
    # Create and synthesize the quantum program
    qmod = create_model(main)
    qprog = synthesize(qmod)
    
    # Execute and show results
    job = execute(qprog)
    results = job.result()[0].value
    
    print("Grover Search Results:")
    print("Found solutions that satisfy ((a + b) + (c & 6)) % 4) | (4 & c)) == 4:")
    
    for state, amplitude in results.parsed_counts.items():
        a_val = state['a']
        b_val = state['b'] 
        c_val = state['c']
        
        # Verify the predicate
        result = ((a_val + b_val) + (c_val & 6)) % 4
        final = result | (4 & c_val)
        
        if final == 4:
            print(f"a={a_val}, b={b_val}, c={c_val} -> {final} == 4 ✓ (probability: {amplitude})")
        else:
            print(f"a={a_val}, b={b_val}, c={c_val} -> {final} != 4 (probability: {amplitude})")