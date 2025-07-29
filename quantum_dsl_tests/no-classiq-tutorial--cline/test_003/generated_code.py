import time
from classiq import *

# Start timing for generation
start_time = time.time()

@qfunc
def main(x: Output[QNum], y: Output[QNum], res: Output[QNum]):
    # Initialize quantum number x to value 2
    prepare_int(2, x)
    
    # Initialize quantum number y to value 7  
    prepare_int(7, y)
    
    # Compute res = x + y using quantum arithmetic
    res |= x + y

# Create the quantum model
model = create_model(main)
print("Model created successfully")

# Synthesize the quantum program
qprog = synthesize(model)
print("Synthesis completed successfully")

# Execute the program
job = execute(qprog)
results = job.result()

# End timing
end_time = time.time()
generation_time = end_time - start_time

print(f"\n=== Quantum Arithmetic Results ===")
print(f"Execution results: {results}")

# Parse and display the results
if hasattr(results, 'counts'):
    counts = results.counts
    print(f"Counts: {counts}")
    
    # Analyze the results
    total_shots = sum(counts.values())
    print(f"\nTotal shots: {total_shots}")
    
    # Expected result: x=2, y=7, res=9
    # In binary: x=10, y=111, res=1001
    expected_result = "1001"  # 9 in binary
    
    print("Result analysis:")
    for state, count in counts.items():
        probability = count / total_shots
        print(f"  |{state}⟩: {count} shots ({probability:.3f})")
        
        # Check if this matches expected result (res should be 9)
        if expected_result in state:
            print(f"  ✓ Expected result found: {expected_result} (decimal 9)")

print(f"\nGeneration time: {generation_time:.3f} seconds")
