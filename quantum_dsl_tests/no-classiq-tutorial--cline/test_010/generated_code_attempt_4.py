from classiq import *

@qfunc
def main(x: Output[QNum[3]], y: Output[QNum]):
    # Allocate x and apply hadamard_transform
    allocate(3, x)
    hadamard_transform(x)
    
    # Compute y = x² + 1 using quantum arithmetic
    # Create a temporary variable for x squared
    x_temp = QNum("x_temp")
    x_temp |= x
    
    # Compute x² by multiplying x with x_temp
    x_squared = x * x_temp
    
    # Then add 1 to get y = x² + 1
    y |= x_squared + 1

# Create the quantum model
qmod = create_model(main)

# Synthesize with depth optimization (minimize circuit depth)
from classiq import synthesize, set_constraints

# Set constraints for depth optimization
constraints = Constraints(optimization_parameter="depth")
qmod = set_constraints(qmod, constraints)

# Synthesize the circuit
qprog = synthesize(qmod)

# Show the resulting circuit
print("Circuit synthesized with depth optimization:")

# Get circuit statistics
from classiq import get_circuit_stats
stats = get_circuit_stats(qprog)
print(f"Circuit depth: {stats.depth}")
print(f"Circuit width (number of qubits): {stats.width}")

# Display the circuit
show(qprog)

# Print depth/width tradeoff information
print(f"\nDepth/Width Tradeoff Analysis:")
print(f"- Circuit Depth: {stats.depth}")
print(f"- Circuit Width: {stats.width} qubits")
print("- Optimized for minimal depth, which may result in higher qubit count")
