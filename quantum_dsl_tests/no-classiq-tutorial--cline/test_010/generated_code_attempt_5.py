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

# Try to access circuit properties directly from the quantum program
try:
    # Check what attributes are available
    print("Available attributes:", [attr for attr in dir(qprog) if not attr.startswith('_')])
    
    # Try different ways to get circuit info
    if hasattr(qprog, 'data'):
        print(f"Circuit data available")
        if hasattr(qprog.data, 'depth'):
            print(f"Circuit depth: {qprog.data.depth}")
        if hasattr(qprog.data, 'width'):
            print(f"Circuit width: {qprog.data.width}")
    
    # Try to get the number of qubits
    if hasattr(qprog, 'num_qubits'):
        print(f"Number of qubits: {qprog.num_qubits}")
        
except Exception as e:
    print(f"Error accessing circuit properties: {e}")

# Display the circuit
show(qprog)

# Print depth/width tradeoff information
print(f"\nDepth/Width Tradeoff Analysis:")
print("- Circuit optimized for minimal depth")
print("- This optimization may result in higher qubit count")
print("- The synthesis process balances depth vs width based on the optimization parameter")
