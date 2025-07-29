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
def diffuser(x: QArray[QBit]):
    """
    Grover diffusion operator
    """
    within_apply(
        lambda: inplace_prepare_state([1.0] + [0.0] * (2**x.len - 1), 0.0, x),
        lambda: phase_oracle_diffuser(x)
    )

@qfunc
def phase_oracle_diffuser(x: QArray[QBit]):
    """
    Phase oracle for diffuser - flips phase of |0...0> state
    """
    aux = QBit("aux")
    within_apply(
        lambda: H(aux),
        lambda: X(aux) if all(qubit == 0 for qubit in x) else None
    )

@qfunc
def grover_algorithm():
    """
    Main Grover search algorithm with 3 iterations
    """
    # Initialize quantum registers
    a = QNum("a", 2, False)  # 2 qubits for a
    b = QNum("b", 2, False)  # 2 qubits for b  
    c = QNum("c", 3, False)  # 3 qubits for c
    
    # Initialize superposition
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Apply Grover iterations (3 times)
    for i in range(3):
        # Apply phase oracle
        phase_oracle(a, b, c)
        
        # Apply diffuser
        all_qubits = QArray("all_qubits")
        all_qubits |= a.as_array() + b.as_array() + c.as_array()
        diffuser(all_qubits)

@qfunc
def main(a: Output[QNum], b: Output[QNum], c: Output[QNum]):
    allocate(2, a)
    allocate(2, b)
    allocate(3, c)
    grover_algorithm()

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