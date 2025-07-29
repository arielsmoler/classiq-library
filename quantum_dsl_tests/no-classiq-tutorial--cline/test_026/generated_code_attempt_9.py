from classiq import *
import numpy as np

# Define the QStruct with two qbit arrays x and y, each of size 3
@QStruct
class QVars:
    x: QArray[QBit]
    y: QArray[QBit]

# Define the foo function that applies phase based on the sum of x and y
@qfunc
def foo(qvars: QVars):
    # Convert QBit arrays to QNums for arithmetic
    x_num = QNum("x_num")
    y_num = QNum("y_num")
    
    # Bind the arrays to numbers
    bind(qvars.x, x_num)
    bind(qvars.y, y_num)
    
    # Calculate the sum of x and y
    sum_val = x_num + y_num
    # Apply phase based on the sum
    phase(np.pi / 4 * sum_val)
    
    # Bind back
    bind(x_num, qvars.x)
    bind(y_num, qvars.y)

# Main function
@qfunc
def main(qvars: Output[QVars]):
    # Initialize the qstruct with 3-bit arrays
    allocate(3, qvars.x)
    allocate(3, qvars.y)
    
    # Apply Hadamard transform on the qstruct before calling foo
    hadamard_transform(qvars)
    
    # Call foo function
    foo(qvars)
    
    # Apply Hadamard transform on the qstruct after calling foo
    hadamard_transform(qvars)

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
