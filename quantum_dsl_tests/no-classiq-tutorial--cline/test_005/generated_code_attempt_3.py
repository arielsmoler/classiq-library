import time
from classiq import *

# Record generation start time
generation_start_time = time.time()

@qfunc
def add_two_numbers(x: QNum, y: QNum, res: Output[QNum]):
    """Add two quantum numbers"""
    res |= x + y

@qfunc
def main(result: Output[QNum]):
    # Initialize the input values
    x = QNum("x")
    y = QNum("y") 
    z = QNum("z")
    
    x |= 3
    y |= 5
    z |= 2
    
    # Use within_apply to compute x + y + z
    # First compute temp = x + y, then result = temp + z
    # The temporary variable will be automatically uncomputed
    temp = QNum("temp")
    
    within_apply(
        within=lambda: add_two_numbers(x, y, temp),
        apply=lambda: add_two_numbers(temp, z, result)
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
success = False

print("Result analysis:")
for state, count in results.counts.items():
    probability = count / total_shots
    # For the result register, we need to extract the relevant bits
    # The result should be 10 (decimal) = 1010 (binary)
    decimal_value = int(state, 2) if state != '0' * len(state) else 0
    print(f"  |{state}⟩: {count} shots ({probability:.3f}) -> decimal: {decimal_value}")
    
    # Check if the result contains 10 (looking at the rightmost bits for the result)
    if '1010' in state or decimal_value == 10:
        success = True

# Also check if any state represents 10 in the result register
for state, count in results.counts.items():
    # Extract the last 4 bits (enough for result up to 15)
    if len(state) >= 4:
        result_bits = state[-4:]
        result_value = int(result_bits, 2)
        if result_value == 10:
            success = True
            print(f"Found result 10 in state |{state}⟩ (last 4 bits: {result_bits} = {result_value})")

if success:
    print(f"\n✓ SUCCESS: Found expected result 10 in the measurement outcomes")
else:
    print(f"\n✗ FAILURE: Expected result 10 not found in measurement outcomes")

print(f"\nGeneration time: {generation_time:.3f} seconds")
