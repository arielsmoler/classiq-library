"""
9-Face Dice Quantum Program using Classiq

This program creates a quantum simulation of a 9-face dice throw.
Since 9 is not a power of 2, we need 4 qubits (2^4 = 16 states) and 
filter out states 9-15 to get uniform distribution over states 0-8.
We then map these to dice faces 1-9.
"""

from classiq import *
import numpy as np

# Number of qubits needed (4 qubits give us 16 states, we'll use 9 of them)
NUM_QUBITS = 4

@qfunc
def prepare_nine_states(target: Output[QNum]) -> None:
    """
    Prepare equal superposition over 9 states (0-8) representing dice faces 1-9.
    Uses rejection sampling approach - we create superposition over 16 states
    and post-select on the first 9 states.
    """
    # Allocate qubits for our quantum number
    allocate(NUM_QUBITS, target)
    
    # Create equal superposition over all 16 states
    hadamard_transform(target)

@qfunc 
def main(dice_result: Output[QNum]) -> None:
    """
    Main function that simulates a 9-face dice throw.
    The result will be a quantum number from 0-8, representing dice faces 1-9.
    """
    prepare_nine_states(dice_result)

# Create the quantum model
model = create_model(main)

# Set constraints to optimize for fewer qubits
constraints = Constraints(max_width=10)
model = set_constraints(model, constraints)

# Synthesize the quantum program
quantum_program = synthesize(model)

def simulate_dice_throw(num_shots: int = 1000) -> dict:
    """
    Execute the quantum program and return dice throw results.
    
    Args:
        num_shots: Number of times to run the quantum program
        
    Returns:
        Dictionary with dice faces (1-9) and their counts, 
        filtered to only include valid dice outcomes
    """
    # Execute the quantum program
    job = execute(quantum_program)
    results = job.result()
    
    # Get the raw counts (will include states 0-15)
    raw_counts = results[0].value.parsed_counts
    
    # Get the actual number of shots from results
    num_shots = len(raw_counts)
    
    # Filter to only include valid dice outcomes (0-8) and map to dice faces (1-9)
    dice_counts = {}
    total_valid = 0
    
    for state in raw_counts:
        # Extract the quantum number value from the state
        state_value = state.state['dice_result']
        count = state.shots
        
        # Only keep states 0-8 (representing dice faces 1-9)
        if 0 <= state_value <= 8:
            dice_face = state_value + 1  # Map 0-8 to 1-9
            dice_counts[dice_face] = dice_counts.get(dice_face, 0) + 1
            total_valid += 1
    
    # Calculate success rate (should be 9/16 = 56.25%)
    success_rate = total_valid / num_shots
    
    return {
        'dice_counts': dice_counts,
        'total_valid_throws': total_valid,
        'success_rate': success_rate,
        'num_shots': num_shots
    }

def print_dice_results(results: dict) -> None:
    """Pretty print the dice throw results."""
    print("\n🎲 9-Face Dice Quantum Simulation Results 🎲")
    print("=" * 45)
    print(f"Total shots: {results['num_shots']}")
    print(f"Valid dice throws: {results['total_valid_throws']}")
    print(f"Success rate: {results['success_rate']:.2%}")
    print("\nDice Face Distribution:")
    print("-" * 25)
    
    dice_counts = results['dice_counts']
    for face in range(1, 10):
        count = dice_counts.get(face, 0)
        percentage = (count / results['total_valid_throws']) * 100 if results['total_valid_throws'] > 0 else 0
        bar = "█" * int(percentage / 2)  # Scale bar for display
        print(f"Face {face}: {count:4d} ({percentage:5.1f}%) {bar}")

if __name__ == "__main__":
    # Show the quantum program
    print("Quantum Program Structure:")
    show(quantum_program)
    
    # Run the simulation
    print("\nRunning 9-face dice simulation...")
    results = simulate_dice_throw(num_shots=2000)
    print_dice_results(results)
    
    # Additional analysis
    print(f"\nTheoretical vs Actual:")
    print(f"Expected success rate: {9/16:.2%}")
    print(f"Actual success rate: {results['success_rate']:.2%}")
    print(f"Expected count per face: {results['total_valid_throws']/9:.1f}")