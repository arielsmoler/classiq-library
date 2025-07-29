from classiq import *

@qfunc
def main(x: Output[QNum], y: Output[QNum], res: Output[QNum]):
    # Initialize x to value 2
    prepare_int(2, x)
    
    # Initialize y to value 7
    prepare_int(7, y)
    
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