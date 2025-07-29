import time
from classiq import *

# Start timing for generation
start_time = time.time()

@qfunc
def main(x: Output[QNum], y: Output[QNum], res: Output[QNum]):
    # Initialize quantum number x to value 2 (using modern syntax)
    x |= 2
    
    # Initialize quantum number y to value 7 (using modern syntax)
    y |= 7
    
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

# Check parsed states for cleaner output
if len(results) > 0 and hasattr(results[0], 'value') and hasattr(results[0].value, 'parsed_states'):
    parsed_states = results[0].value.parsed_states
    print(f"\nParsed states: {parsed_states}")
    
    for state, values in parsed_states.items():
        if 'x' in values and 'y' in values and 'res' in values:
            x_val = values['x']
            y_val = values['y']
            res_val = values['res']
            print(f"✓ SUCCESS: x={x_val}, y={y_val}, res={res_val}")
            if x_val == 2 and y_val == 7 and res_val == 9:
                print("✓ CORRECT: 2 + 7 = 9 computed successfully!")

print(f"\nGeneration time: {generation_time:.3f} seconds")
