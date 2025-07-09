"""
3-Qubit GHZ State Implementation #1: Standard Approach
Using H gate on first qubit followed by CNOT gates

The GHZ state is: |GHZ⟩ = (|000⟩ + |111⟩)/√2
This is a maximally entangled state of 3 qubits.
"""

from classiq import *

@qfunc
def create_ghz_state_v1(qubits: Output[QArray[QBit]]) -> None:
    """
    Create 3-qubit GHZ state using standard approach:
    1. Apply H gate to first qubit to create superposition
    2. Apply CNOT gates to entangle all qubits
    
    Circuit: H(q0) -> CNOT(q0,q1) -> CNOT(q1,q2)
    """
    # Allocate 3 qubits
    allocate(3, qubits)
    
    # Apply Hadamard to first qubit: |0⟩ → (|0⟩ + |1⟩)/√2
    H(qubits[0])
    
    # Apply CNOT from first to second qubit
    CX(qubits[0], qubits[1])
    
    # Apply CNOT from second to third qubit
    CX(qubits[1], qubits[2])

@qfunc
def main(result: Output[QArray[QBit]]) -> None:
    """Main function to create and measure the GHZ state."""
    create_ghz_state_v1(result)

# Create and synthesize the quantum program
model = create_model(main)
quantum_program = synthesize(model)

def test_ghz_state_v1():
    """Test the GHZ state implementation."""
    print("🔬 Testing 3-Qubit GHZ State - Implementation #1 (Standard Approach)")
    print("=" * 70)
    
    # Show the quantum program structure
    print("Quantum Program Structure:")
    show(quantum_program)
    
    # Execute the quantum program
    print("\nExecuting quantum program...")
    job = execute(quantum_program)
    results = job.result()
    
    # Parse results
    raw_counts = results[0].value.parsed_counts
    
    print(f"\nResults from {len(raw_counts)} measurement outcomes:")
    print("-" * 50)
    
    # Expected outcomes for GHZ state: should see only |000⟩ and |111⟩
    total_shots = 0
    ghz_states = 0
    
    for state in raw_counts:
        # Extract the qubit values
        qubit_values = state.state['result']
        count = state.shots
        total_shots += count
        
        # Convert to binary string for display
        binary_str = ''.join(str(bit) for bit in qubit_values)
        
        # Check if this is a valid GHZ state (000 or 111)
        if binary_str in ['000', '111']:
            ghz_states += count
            marker = "✓ GHZ"
        else:
            marker = "✗ Error"
        
        print(f"|{binary_str}⟩: {count:4d} shots ({count/total_shots*100:5.1f}%) {marker}")
    
    # Calculate fidelity
    fidelity = ghz_states / total_shots if total_shots > 0 else 0
    print(f"\nGHZ State Fidelity: {fidelity:.3f} ({fidelity*100:.1f}%)")
    print(f"Expected: Only |000⟩ and |111⟩ states should appear")
    
    # Theoretical analysis
    print(f"\nTheoretical expectation:")
    print(f"- |000⟩ probability: ~50%")
    print(f"- |111⟩ probability: ~50%")
    print(f"- All other states: 0%")
    
    return results

if __name__ == "__main__":
    test_ghz_state_v1()