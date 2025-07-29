from classiq import *
import numpy as np

# Define the foo function that applies phase based on the sum of two qnums
@qfunc
def foo(x: QNum, y: QNum):
    # Calculate the sum of x and y
    sum_val = x + y
    # Apply phase based on the sum
    phase(np.pi / 4 * sum_val)

# Main function
@qfunc
def main(x: Output[QNum], y: Output[QNum]):
    # Initialize two 3-bit qnums using allocate instead of allocate_num
    allocate(3, x)
    allocate(3, y)
    
    # Apply Hadamard transform on both qnums before calling foo
    hadamard_transform(x)
    hadamard_transform(y)
    
    # Call foo function
    foo(x, y)
    
    # Apply Hadamard transform on both qnums after calling foo
    hadamard_transform(x)
    hadamard_transform(y)

# Create and synthesize the quantum model
qmod = create_model(main)
qprog = synthesize(qmod)

# Execute the quantum program
job = execute(qprog)
results = job.result()[0].value

# Print the most probable result
print("Most probable result:")
print(f"Counts: {results.counts}")
print(f"Most probable state: {max(results.counts, key=results.counts.get)}")
print(f"Probability: {max(results.counts.values()) / sum(results.counts.values()):.4f}")
