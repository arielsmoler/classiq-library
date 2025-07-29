from classiq import *

@qfunc
def main(x: Output[QNum], y: Output[QNum], res: Output[QNum]):
    # Initialize x to value 2 (requires 2 qubits for value 2)
    allocate(2, x)
    prepare_int(2, x)
    
    # Initialize y to value 7 (requires 3 qubits for value 7)  
    allocate(3, y)
    prepare_int(7, y)
    
    # Allocate qubits for result (needs 4 qubits to hold sum up to 9)
    allocate(4, res)
    
    # Compute res = x + y using quantum arithmetic
    res |= x + y

# Create and synthesize the quantum program
qmod = create_model(main)
qprog = synthesize(qmod)

# Execute the program
job = execute(qprog)
results = job.result()[0].value

print("Execution results:")
print(f"x = {results.x}")
print(f"y = {results.y}")  
print(f"res = x + y = {results.res}")