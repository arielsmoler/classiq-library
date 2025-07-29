import time
from classiq import *

def run_test():
    start_time = time.time()
    
    # Create the quantum model
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
    print("Model created successfully")
    
    # Synthesize the circuit
    qprog = synthesize(model)
    print("Synthesis completed successfully")
    
    # Show the circuit
    show(qprog)
    
    end_time = time.time()
    generation_time = end_time - start_time
    print(f"\nGeneration time: {generation_time:.3f} seconds")

if __name__ == "__main__":
    run_test()
