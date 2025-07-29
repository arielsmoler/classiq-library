from classiq import *

@qfunc
def main(x: Output[QNum], y: Output[QNum], res: Output[QNum]):
    # Initialize x to value 2 using modern assignment syntax
    x |= 2
    
    # Initialize y to value 7 using modern assignment syntax
    y |= 7
    
    # Compute res = x + y using quantum arithmetic
    res |= x + y

# Create and synthesize the quantum program
qmod = create_model(main)
qprog = synthesize(qmod)

# Execute the program
job = execute(qprog)
result = job.result()

print("Execution results:")
print(f"Result: {result}")

# Try to access the parsed results
for sample in result:
    parsed = sample.value
    print(f"Parsed sample: {parsed}")
    if hasattr(parsed, 'x'):
        print(f"x = {parsed.x}")
    if hasattr(parsed, 'y'):
        print(f"y = {parsed.y}")
    if hasattr(parsed, 'res'):
        print(f"res = x + y = {parsed.res}")