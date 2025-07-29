from classiq import *

@qfunc
def main(res: Output[QNum]):
    # Declare x as a 2-qubit quantum number
    x = QNum("x", 2, False, 0)
    
    # Declare y as a 3-qubit quantum number  
    y = QNum("y", 3, False, 0)
    
    # Initialize x to equal superposition of 0 and 2
    prepare_state([0.5**0.5, 0, 0.5**0.5, 0], 0, x)
    
    # Initialize y to equal superposition of 1, 2, 3, and 6
    probabilities_y = [0, 0.5**0.5, 0.5**0.5, 0.5**0.5, 0, 0, 0.5**0.5, 0]
    prepare_state(probabilities_y, 0, y)
    
    # Compute res = x + y
    res |= x + y

# Create and synthesize the quantum program
qmod = create_model(main)
qprog = synthesize(qmod)

# Execute the program
job = execute(qprog)
results = job.result()[0].value
print("Results:", results)