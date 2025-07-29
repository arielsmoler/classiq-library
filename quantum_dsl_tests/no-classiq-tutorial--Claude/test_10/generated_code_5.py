from classiq import (
    QNum,
    Output,
    allocate,
    hadamard_transform,
    synthesize,
    qfunc,
    create_model,
    show,
    set_constraints,
    Constraints,
    OptimizationParameter,
    numeric_literal
)

@qfunc
def main(x: Output[QNum[3]], y: Output[QNum]):
    # Allocate x as a 3-qubit quantum number
    allocate(3, x)
    
    # Apply Hadamard transform to x
    hadamard_transform(x)
    
    # Compute y = x² + 1 using quantum arithmetic
    # First allocate y with enough qubits to hold the result
    allocate(6, y)  # x² can be up to 49 for 3-bit x, so need 6 bits
    
    # Create a separate variable for x to use in multiplication
    x_copy: QNum[3]
    allocate(3, x_copy)
    x_copy |= x
    
    # Compute x² step by step
    x_squared: QNum[6]
    allocate(6, x_squared)
    x_squared |= x * x_copy
    
    # Add 1 to get final result
    one = numeric_literal(1, 6)
    y |= x_squared + one

# Create the model
model = create_model(main)

# Set synthesis constraints to optimize for depth
constraints = Constraints(optimization_parameter=OptimizationParameter.DEPTH)
model = set_constraints(model, constraints)

# Synthesize the quantum program
qprog = synthesize(model)

# Show the circuit
show(qprog)

# Print circuit statistics
print(f"Circuit depth: {qprog.data.depth}")
print(f"Circuit width (number of qubits): {qprog.data.width}")
print(f"Gate count: {qprog.data.gate_count}")
print("\nDepth/Width Tradeoff Analysis:")
print("- Optimizing for depth typically results in using more qubits (ancillas)")
print("- This allows parallel execution of operations that would otherwise be sequential")
print("- The tradeoff is increased qubit requirements vs reduced circuit depth")