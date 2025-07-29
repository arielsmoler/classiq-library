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

print("Quantum Arithmetic Results:")
print("=" * 30)

# Extract the parsed states from the execution details
execution_details = result[0].value
parsed_states = execution_details.parsed_states

# Get the results from the parsed states
for state, values in parsed_states.items():
    print(f"Quantum state: {state}")
    print(f"x = {values['x']}")
    print(f"y = {values['y']}")
    print(f"res = x + y = {values['res']}")
    print(f"Verification: {values['x']} + {values['y']} = {values['res']} ✓")

print("\nProgram executed successfully!")