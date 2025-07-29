import time
from classiq import *

# Record generation start time
generation_start_time = time.time()

@qfunc
def add_two_numbers(x: QNum, y: QNum, res: Output[QNum]):
    """Add two quantum numbers"""
    res |= x + y

@qfunc
def main(x: Output[QNum], y: Output[QNum], z: Output[QNum], result: Output[QNum]):
    # Initialize the input values
    prepare_int(3, x)
    prepare_int(5, y) 
    prepare_int(2, z)
    
    # Use within_apply to compute x + y + z
    # First compute temp = x + y, then result = temp + z
    # The temporary variable will be automatically uncomputed
    within_apply(
        compute=lambda: add_two_numbers(x, y, temp),
        action=lambda: add_two_numbers(temp, z, result)
    )

# Create the quantum model
model = create_model(main)
print("Model created successfully")

# Record generation end time
generation_end_time = time.time()
generation_time = generation_end_time - generation_start_time

# Synthesize the quantum program
qprog = synthesize(model)
print("Synthesis completed successfully")

# Execute the quantum program
job = execute(qprog)
results = job.result()[0].value

print(f"\n=== Within-Apply Addition Results ===")
print(f"Computing: x + y + z where x=3, y=5, z=2")
print(f"Expected result: 10")
print(f"Counts: {results.counts}")

# Analyze results
total_shots = sum(results.counts.values())
print(f"\nTotal shots: {total_shots}")

# Check if we got the expected result (10 in binary)
expected_binary = format(10, 'b')
success = False

print("Result analysis:")
for state, count in results.counts.items():
    probability = count / total_shots
    decimal_value = int(state, 2) if state != '0' * len(state) else 0
    print(f"  |{state}⟩: {count} shots ({probability:.3f}) -> decimal: {decimal_value}")
    
    if decimal_value == 10:
        success = True

if success:
    print(f"\n✓ SUCCESS: Found expected result 10 in the measurement outcomes")
else:
    print(f"\n✗ FAILURE: Expected result 10 not found in measurement outcomes")

print(f"\nGeneration time: {generation_time:.3f} seconds")
