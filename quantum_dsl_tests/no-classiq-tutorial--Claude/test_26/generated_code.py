from classiq import *

# Define the QStruct with two qnums x and y, each of size 3
@qstruct
class QVars:
    x: QNum[3]
    y: QNum[3]

# Define function foo that applies phase based on sum of x and y
@qfunc
def foo(qvars: QVars):
    # Apply phase based on the sum of x and y
    phase_oracle = lambda x, y: x + y
    apply_to_all(QM_PHASE_Z, [qvars.x, qvars.y], phase_oracle)

# Main function that initializes qstruct and applies H transforms
@qfunc
def main(qvars: Output[QVars]):
    # Initialize the qstruct
    allocate(6, qvars)
    
    # Apply Hadamard transform on the qstruct before foo
    hadamard_transform(qvars)
    
    # Call foo function
    foo(qvars)
    
    # Apply Hadamard transform on the qstruct after foo
    hadamard_transform(qvars)

# Synthesize and execute
qmod = create_model(main)
qprog = synthesize(qmod)
job = execute(qprog)
result = job.result()

# Print the most probable result
print("Most probable result:", result[0].state)