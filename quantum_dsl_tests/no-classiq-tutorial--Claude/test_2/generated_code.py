from classiq import *

@qfunc
def bell_state(qubits: Output[QArray[QBit, 2]]):
    # Initialize qubits
    allocate(2, qubits)
    
    # Apply Hadamard gate to first qubit
    H(qubits[0])
    
    # Apply CNOT gate with first qubit as control, second as target
    CX(qubits[0], qubits[1])

@qfunc
def main(qubits: Output[QArray[QBit, 2]]):
    bell_state(qubits)

# Create and synthesize the quantum model
qmod = create_model(main)
qprog = synthesize(qmod)

# Execute the program
job = execute(qprog)
results = job.result()

# Print the results
print("Bell State Results:")
print(f"Counts: {results[0].value.counts}")

# Verify only |00⟩ and |11⟩ states appear
counts = results[0].value.counts
expected_states = {'00', '11'}
actual_states = set(counts.keys())

print(f"\nExpected states: {expected_states}")
print(f"Actual states: {actual_states}")
print(f"Bell state verification: {'PASSED' if actual_states == expected_states else 'FAILED'}")

# Show probabilities
total_shots = sum(counts.values())
for state, count in counts.items():
    probability = count / total_shots
    print(f"State |{state}⟩: {count}/{total_shots} = {probability:.3f}")