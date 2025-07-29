from classiq import *

@qfunc
def main(q: Output[QArray[QBit]]) -> None:
    # Allocate 4 qubits
    allocate(4, q)
    
    # Define the Pauli Hamiltonian H = 0.5XZXX + 0.25YIZI + 0.3XIZY
    hamiltonian = [
        PauliTerm([Pauli.X, Pauli.Z, Pauli.X, Pauli.X], 0.5),
        PauliTerm([Pauli.Y, Pauli.I, Pauli.Z, Pauli.I], 0.25),
        PauliTerm([Pauli.X, Pauli.I, Pauli.Z, Pauli.Y], 0.3),
    ]
    
    # Apply Suzuki-Trotter evolution
    suzuki_trotter(
        hamiltonian,
        evolution_coefficient=3,
        order=2,
        repetitions=4,
        qbv=q,
    )

# Create the quantum model
model = create_model(main)

# Synthesize the circuit
qprog = synthesize(model)

print("Circuit synthesized successfully!")
print(f"Circuit depth: {qprog.depth}")
print(f"Number of qubits: {qprog.width}")
print(f"Number of gates: {len(qprog.instructions)}")