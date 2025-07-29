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
def main(a: Output[QNum], b: Output[QNum], c: Output[QNum]):
    # Allocate qubits
    allocate(2, a)  # 2 qubits for a (values 0-3)
    allocate(2, b)  # 2 qubits for b (values 0-3)
    allocate(3, c)  # 3 qubits for c (values 0-7)
    
    # Initialize in superposition
    hadamard_transform(a)
    hadamard_transform(b)
    hadamard_transform(c)
    
    # Simple oracle application (without full Grover for now)
    # This will at least test if the oracle function works
    aux = QBit("aux")
    allocate(1, aux)
    oracle_function(a, b, c, aux)

# Create and synthesize the quantum program
qmod = create_model(main)
qprog = synthesize(qmod)

# Execute the program
job = execute(qprog)
results = job.result()

print("Oracle Test Results:")
print(f"Results type: {type(results)}")
print(f"Results: {results}")

# Try to access counts in different ways
try:
    if hasattr(results, 'counts'):
        counts = results.counts
    elif hasattr(results, 'parsed_counts'):
        counts = results.parsed_counts
    elif len(results) > 0 and hasattr(results[0], 'counts'):
        counts = results[0].counts
    elif len(results) > 0 and hasattr(results[0], 'parsed_counts'):
        counts = results[0].parsed_counts
    else:
        print("Available attributes:", dir(results))
        if len(results) > 0:
            print("First result attributes:", dir(results[0]))
        counts = {}
    
    print(f"Counts: {counts}")
    
    # Analyze results to find solutions
    print("\nAnalyzing solutions:")
    for state, count in counts.items():
        if count > 0:
            # Parse the state (8 qubits total: 2 for a, 2 for b, 3 for c, 1 for aux)
            state_bits = state
            aux_val = int(state_bits[0], 2)  # First bit is aux
            a_val = int(state_bits[-2:], 2)  # Last 2 bits for a
            b_val = int(state_bits[-4:-2], 2)  # Next 2 bits for b  
            c_val = int(state_bits[-7:-4], 2)  # Next 3 bits for c
            
            # Verify the predicate
            result = ((a_val + b_val) + (c_val & 6)) % 4
            final = result | (4 & c_val)
            
            print(f"State {state}: aux={aux_val}, a={a_val}, b={b_val}, c={c_val}")
            print(f"  Calculation: (({a_val} + {b_val}) + ({c_val} & 6)) % 4 | (4 & {c_val}) = {final}")
            print(f"  Satisfies predicate (== 4): {final == 4}")
            print(f"  Oracle flipped aux: {aux_val == 1}")
            print(f"  Count: {count}")
            print()

except Exception as e:
    print(f"Error accessing results: {e}")

# Also test all possible combinations classically to verify our logic
print("\nClassical verification of all combinations:")
solutions = []
for a_val in range(4):
    for b_val in range(4):
        for c_val in range(8):
            result = ((a_val + b_val) + (c_val & 6)) % 4
            final = result | (4 & c_val)
            if final == 4:
                solutions.append((a_val, b_val, c_val))
                print(f"Solution: a={a_val}, b={b_val}, c={c_val}")

print(f"\nTotal solutions found: {len(solutions)}")
