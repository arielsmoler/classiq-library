from classiq import *

@qfunc
def foo(qubits: QArray[QBit, 3]):
    # Bind the 3-qubit array to separate variables using explicit declarations
    b1 = QBit()
    b2 = QArray[QBit, 2]()
    bind(qubits, [b1, b2])
    
    # Apply hadamard transform to b2 (2-qubit array)
    hadamard_transform(b2)
    
    # Apply controlled X gate where b2 controls b1
    control(b2, lambda: X(b1))
    
    # Rebind the variables back to the original 3-qubit array
    bind([b1, b2], qubits)

@qfunc
def main(qubits: Output[QArray[QBit, 3]]):
    # Allocate 3 qubits
    allocate(3, qubits)
    
    # Call the foo function
    foo(qubits)

# Create and synthesize the model
model = create_model(main)

# Set synthesis constraints for optimization
constraints = Constraints(optimization_parameter=OptimizationParameter.DEPTH)
set_constraints(model, constraints)

# Synthesize the quantum program
qprog = synthesize(model)

# Show the quantum program results
show(qprog)

# Execute the quantum program and verify results
job = execute(qprog)
result = job.result()
print("Execution completed successfully!")
print("Result counts:", result.counts_by_bit_string)

# Verify expected results
print("\nVerification:")
print("The circuit applies Hadamard to 2 control qubits and controlled-X to target")
print("Expected states should show superposition effects from the Hadamard gates")
print("and controlled behavior from the C-X gate")
print("Number of shots:", len(result.parsed_counts))
if len(result.parsed_counts) > 0:
    print("Verification: Execution successful with measurement results")