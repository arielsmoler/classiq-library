from classiq import *

@qfunc
def main(x: Output[QNum[3]], y: Output[QNum]):
    # Allocate x and apply hadamard_transform
    allocate(3, x)
    hadamard_transform(x)
    
    # Compute y = x² + 1 using quantum arithmetic
    # Use a proper approach for squaring by creating separate variables
    x_copy = QNum("x_copy")
    x_copy |= x
    
    # Compute x² by multiplying x with x_copy (avoiding x * x issue)
    x_squared = x * x_copy
    
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
print(f"Circuit width: {qprog.data.width} qubits")

# Try to get depth information if available
if hasattr(qprog.data, 'depth'):
    print(f"Circuit depth: {qprog.data.depth}")
else:
    print("Circuit depth information not directly available")

# Display the circuit
show(qprog)

# Print depth/width tradeoff information
print(f"\nDepth/Width Tradeoff Analysis:")
print(f"- Circuit Width: {qprog.data.width} qubits")
print("- Circuit optimized for minimal depth")
print("- Depth optimization typically results in higher qubit usage")
print("- The synthesis balances computational depth vs spatial width")
print("\nSynthesis completed successfully with depth optimization!")
