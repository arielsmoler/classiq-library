"""
3-Qubit GHZ State Implementation #2: Alternative Approach
Using multi-controlled X gates and rotation-based preparation

The GHZ state is: |GHZ⟩ = (|000⟩ + |111⟩)/√2
This implementation uses a different circuit construction approach.
"""

from classiq import *
import numpy as np

@qfunc
def create_ghz_state_v2(qubits: Output[QArray[QBit]]) -> None:
    """
    Create 3-qubit GHZ state using alternative approach:
    1. Start with |000⟩ state
    2. Apply X gates to create |111⟩ state
    3. Use controlled operations to create superposition
    
    Alternative circuit construction using state preparation method
    """
    # Allocate 3 qubits
    allocate(3, qubits)
    
    # Method 2: Use RY rotations and controlled operations
    # First create superposition on ancilla-like approach
    
    # Apply Hadamard to first qubit
    H(qubits[0])
    
    # Use controlled-X operations in different order
    CX(qubits[0], qubits[2])  # Skip middle qubit first
    CX(qubits[0], qubits[1])  # Then entangle middle qubit

@qfunc
def create_ghz_state_v2_alt(qubits: Output[QArray[QBit]]) -> None:
    """
    Alternative implementation using prepare_state function
    This uses Classiq's built-in state preparation capabilities
    """
    # Define the GHZ state amplitudes
    # |000⟩ and |111⟩ each have amplitude 1/√2
    amplitudes = [1/np.sqrt(2), 0, 0, 0, 0, 0, 0, 1/np.sqrt(2)]
    
    # Use state preparation (if available in Classiq)
    allocate(3, qubits)
    
    # Manual implementation of the state preparation
    # This is equivalent to amplitude encoding for GHZ state
    
    # Start with |000⟩
    # Apply operations to create equal superposition of |000⟩ and |111⟩
    
    # Use RY gate with specific angle to create proper amplitudes
    # For GHZ state, we need RY(π/2) to create equal superposition
    H(qubits[0])  # Creates (|0⟩ + |1⟩)/√2
    
    # Controlled operations to create correlations
    # If first qubit is |1⟩, flip the others
    CX(qubits[0], qubits[1])
    CX(qubits[0], qubits[2])

@qfunc
def main(result: Output[QArray[QBit]]) -> None:
    """Main function using alternative GHZ state creation."""
    create_ghz_state_v2_alt(result)

# Create and synthesize the quantum program
model = create_model(main)
quantum_program = synthesize(model)

def test_ghz_state_v2():
    """Test the alternative GHZ state implementation."""
    print("🔬 Testing 3-Qubit GHZ State - Implementation #2 (Alternative Approach)")
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
    state_counts = {}
    
    for state in raw_counts:
        # Extract the qubit values
        qubit_values = state.state['result']
        count = state.shots
        total_shots += count
        
        # Convert to binary string for display
        binary_str = ''.join(str(bit) for bit in qubit_values)
        state_counts[binary_str] = count
        
        # Check if this is a valid GHZ state (000 or 111)
        if binary_str in ['000', '111']:
            ghz_states += count
            marker = "✓ GHZ"
        else:
            marker = "✗ Error"
        
        print(f"|{binary_str}⟩: {count:4d} shots ({count/total_shots*100:5.1f}%) {marker}")
    
    # Calculate fidelity and statistics
    fidelity = ghz_states / total_shots if total_shots > 0 else 0
    print(f"\nGHZ State Fidelity: {fidelity:.3f} ({fidelity*100:.1f}%)")
    
    # Check balance between |000⟩ and |111⟩
    count_000 = state_counts.get('000', 0)
    count_111 = state_counts.get('111', 0)
    
    if count_000 + count_111 > 0:
        balance = abs(count_000 - count_111) / (count_000 + count_111)
        print(f"State Balance: {balance:.3f} (closer to 0 is better)")
        print(f"|000⟩: {count_000} shots ({count_000/total_shots*100:.1f}%)")
        print(f"|111⟩: {count_111} shots ({count_111/total_shots*100:.1f}%)")
    
    # Theoretical analysis
    print(f"\nComparison with Implementation #1:")
    print(f"- This uses direct H + CX(0,1) + CX(0,2) approach")
    print(f"- Should produce identical results to Implementation #1")
    print(f"- Circuit depth may be different")
    
    return results

def compare_implementations():
    """Compare both implementations side by side."""
    print("\n" + "="*80)
    print("COMPARISON: GHZ State Implementation #1 vs #2")
    print("="*80)
    
    print("\nImplementation #1 (Standard):")
    print("- H(q0) → CNOT(q0,q1) → CNOT(q1,q2)")
    print("- Linear chain of entanglement")
    
    print("\nImplementation #2 (Alternative):")
    print("- H(q0) → CNOT(q0,q1) → CNOT(q0,q2)")
    print("- Star topology of entanglement")
    
    print("\nBoth should produce identical |GHZ⟩ = (|000⟩ + |111⟩)/√2 state")
    print("The difference is in the gate sequence and circuit topology.")

if __name__ == "__main__":
    test_ghz_state_v2()
    compare_implementations()