from classiq import *

@qfunc
def main(x: Output[QNum[3]], y: Output[QNum]):
    # Allocate x and apply hadamard_transform
    allocate(3, x)
    hadamard_transform(x)
    
    # Compute y = x² + 1 using quantum arithmetic
    # First compute x²
    x_squared = x * x
    
    # Then add 1 to get y = x² + 1
    y |= x_squared + 1

# Create the quantum model
qmod = create_model(main)

# Synthesize with depth optimization (minimize circuit depth)
from classiq.synthesis import SynthesisOptions, OptimizationParameter

synthesis_options = SynthesisOptions(
    optimization_parameter=OptimizationParameter.DEPTH
)

# Synthesize the circuit
qprog = synthesize(qmod, synthesis_options=synthesis_options)

# Show the resulting circuit
print("Circuit synthesized with depth optimization:")
print(f"Circuit depth: {qprog.depth}")
print(f"Circuit width (number of qubits): {qprog.width}")

# Display the circuit
show(qprog)

# Print depth/width tradeoff information
print(f"\nDepth/Width Tradeoff Analysis:")
print(f"- Circuit Depth: {qprog.depth}")
print(f"- Circuit Width: {qprog.width} qubits")
print("- Optimized for minimal depth, which may result in higher qubit count")
