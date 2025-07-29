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
    temp = QNum("temp", 5, False, 0)
    
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
    print("Quantum computation result:")
    print(f"x=3, y=5, z=2")
    print(f"res = x + y + z = {3 + 5 + 2}")
    print(f"Measurement counts: {result.counts}")
    
    # Show the most frequent result
    if result.counts:
        most_frequent = max(result.counts.items(), key=lambda x: x[1])
        print(f"Most frequent result: {most_frequent[0]} (appeared {most_frequent[1]} times)")