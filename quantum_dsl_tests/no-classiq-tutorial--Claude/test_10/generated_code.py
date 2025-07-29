from classiq import (
    QNum,
    allocate,
    hadamard_transform,
    synthesize,
    qfunc,
    create_model,
    show,
    set_constraints,
    Constraints,
    OptimizationParameter
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
    
    # Compute x²
    x_squared = x * x
    
    # Compute y = x² + 1
    y |= x_squared + 1

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