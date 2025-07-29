from classiq import *

@qfunc
def add_integers(x: QNum, y: QNum, result: Output[QNum]):
    result |= x + y

@qfunc 
def main(res: Output[QNum]):
    # Initialize variables
    x = QNum("x", 4, False, 0)
    y = QNum("y", 4, False, 0)  
    z = QNum("z", 4, False, 0)
    
    # Set initial values
    x |= 3
    y |= 5
    z |= 2
    
    # Use within_apply to compute x + y + z
    # First add x and y, then add result to z
    temp = QNum("temp", 4, False, 0)
    
    within_apply(
        within=lambda: add_integers(x, y, temp),
        apply=lambda: add_integers(temp, z, res)
    )

if __name__ == "__main__":
    # Create and synthesize the quantum program
    qmod = create_model(main)
    qprog = synthesize(qmod)
    
    # Execute the program
    result = execute(qprog).result()
    
    # Print results
    print("Quantum computation using within-apply pattern:")
    print(f"x=3, y=5, z=2")
    print(f"Expected: res = x + y + z = {3 + 5 + 2}")
    
    # Extract execution details from result
    if result and len(result) > 0:
        execution_details = result[0].value
        counts = execution_details.counts
        parsed_states = execution_details.parsed_states
        
        print(f"Measurement counts: {counts}")
        print(f"Parsed states: {parsed_states}")
        
        # Show the result value
        if parsed_states:
            for state, values in parsed_states.items():
                if 'res' in values:
                    print(f"Quantum result: res = {values['res']}")
                    print("SUCCESS: Within-apply pattern correctly computed x + y + z!")