import time
from classiq import *

# Record start time for generation timing
start_time = time.time()

@qfunc
def bell_state(qubits: Output[QArray[QBit, 2]]):
    """
    Creates a Bell state |+⟩ = (|00⟩ + |11⟩)/√2
    
    Steps:
    1. Allocate 2 qubits (initialized to |00⟩)
    2. Apply Hadamard gate to first qubit -> (|0⟩ + |1⟩)/√2 ⊗ |0⟩
    3. Apply CX gate with first as control, second as target -> (|00⟩ + |11⟩)/√2
    """
    allocate(2, qubits)
    H(qubits[0])  # Hadamard on first qubit
    CX(qubits[0], qubits[1])  # CNOT with first as control, second as target

@qfunc
def main(qubits: Output[QArray[QBit, 2]]):
    bell_state(qubits)

# Create and synthesize the quantum model
model = create_model(main)
print("Model created successfully")

# Synthesize the quantum program
qprog = synthesize(model)
print("Synthesis completed successfully")

# Execute the program to verify Bell state creation
job = execute(qprog)
results = job.result()

print("\n=== Bell State Execution Results ===")
print(f"Counts: {results[0].value.counts}")

# Verify that only |00⟩ and |11⟩ states appear
counts = results[0].value.counts
total_shots = sum(counts.values())

print(f"\nTotal shots: {total_shots}")
print("State probabilities:")
for state, count in counts.items():
    probability = count / total_shots
    print(f"  |{state}⟩: {count} shots ({probability:.3f})")

# Check if only |00⟩ and |11⟩ states appear (allowing for small measurement errors)
expected_states = {'00', '11'}
observed_states = set(counts.keys())
unexpected_states = observed_states - expected_states

if not unexpected_states:
    print("\n✓ SUCCESS: Only expected Bell state components |00⟩ and |11⟩ observed")
else:
    print(f"\n⚠ WARNING: Unexpected states observed: {unexpected_states}")
    print("This might be due to measurement errors or decoherence")

# Calculate generation time
generation_time = time.time() - start_time
print(f"\nGeneration time: {generation_time:.3f} seconds")
