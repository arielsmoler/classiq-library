from classiq import *

@qfunc
def foo(x: QArray[QBit]):
    # Declare variables for binding
    b1 = QBit()
    b2 = QArray[QBit](2)
    
    # Bind the 3-qubit array to separate variables
    bind(x, [b1, b2])
    
    # Apply hadamard transform to b2 (2-qubit array)
    hadamard_transform(b2)
    
    # Apply controlled X gate where b2 controls b1
    control(b2, lambda: X(b1))
    
    # Rebind the variables back to the original 3-qubit array
    bind([b1, b2], x)

@qfunc
def main(res: Output[QArray[QBit]]):
    # Allocate 3 qubits
    allocate(3, res)
    
    # Call the foo function
    foo(res)

# Create and synthesize the quantum model
qmod = create_model(main)
qprog = synthesize(qmod)

# Show the quantum program results
print("Quantum Program:")
show(qprog)

# Execute the program
job = execute(qprog)
results = job.result()

print("\nExecution Results:")
print(results)

# Verify the expected results
print("\nResult Analysis:")
for state, count in results[0].value.counts.items():
    print(f"State |{state}>: {count} counts")
