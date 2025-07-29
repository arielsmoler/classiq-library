import time
from classiq import *

# Start timing for generation
start_time = time.time()

@qfunc
def main(x: Output[QNum], y: Output[QNum], res: Output[QNum]):
    # Declare x as a 2-qubit quantum number (can represent 0, 1, 2, 3)
    allocate(2, x)
    
    # Declare y as a 3-qubit quantum number (can represent 0-7)
    allocate(3, y)
    
    # Initialize x to equal superposition of 0 and 2
    # For equal superposition of 0 and 2, we need |0⟩ + |2⟩ = |00⟩ + |10⟩
    # This means we put the most significant bit in superposition
    H(x[1])  # MSB in superposition using H gate
    
    # Initialize y to equal superposition of 1, 2, 3, and 6
    # 1 = |001⟩, 2 = |010⟩, 3 = |011⟩, 6 = |110⟩
    # We need to create this specific superposition
    prepare_state([0, 0.5, 0.5, 0.5, 0, 0, 0.5, 0], 0.0, y)
    
    # Compute res = x + y
    # res needs enough qubits to hold the sum (max value is 2+6=8, so we need 4 qubits)
    res |= x + y

# Create the quantum model
model = create_model(main)
print("Model created successfully")

# Synthesize the quantum program
qprog = synthesize(model)
print("Synthesis completed successfully")

# End timing for generation
generation_time = time.time() - start_time

# Execute the program
job = execute(qprog)
results = job.result()[0].value

print("\n=== Superposition Arithmetic Results ===")
print(f"Counts: {results.counts}")

# Analyze results
total_shots = sum(results.counts.values())
print(f"\nTotal shots: {total_shots}")

print("Expected combinations:")
print("x=0, y=1 → res=1")
print("x=0, y=2 → res=2") 
print("x=0, y=3 → res=3")
print("x=0, y=6 → res=6")
print("x=2, y=1 → res=3")
print("x=2, y=2 → res=4")
print("x=2, y=3 → res=5")
print("x=2, y=6 → res=8")

print(f"\nGeneration time: {generation_time:.3f} seconds")

# Check if we got the expected results
expected_results = {1, 2, 3, 4, 5, 6, 8}
actual_results = set()

for state_str, count in results.counts.items():
    # Parse the state string to extract res value
    # State format is typically "x_bits,y_bits,res_bits"
    if ',' in state_str:
        parts = state_str.split(',')
        if len(parts) >= 3:
            res_bits = parts[2]
            res_value = int(res_bits, 2)
            actual_results.add(res_value)
    else:
        # If no comma separation, assume it's just the result bits
        res_value = int(state_str, 2)
        actual_results.add(res_value)

print(f"\nActual result values: {sorted(actual_results)}")
print(f"Expected result values: {sorted(expected_results)}")

if expected_results.issubset(actual_results):
    print("✓ SUCCESS: All expected arithmetic results observed")
else:
    missing = expected_results - actual_results
    print(f"⚠ WARNING: Missing expected results: {missing}")
