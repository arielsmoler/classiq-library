from classiq import *

@qfunc
def main(x: Output[QNum], target: Output[QBit]):
    # Initialize x to value 9 using numeric assignment
    x |= 9
    
    # Allocate the target qubit
    allocate(1, target)
    
    # Use control operator to flip target qubit if x equals 9
    control(x == 9, lambda: X(target))

# Create and synthesize the model
model = create_model(main)
quantum_program = synthesize(model)

# Show the circuit
show(quantum_program)