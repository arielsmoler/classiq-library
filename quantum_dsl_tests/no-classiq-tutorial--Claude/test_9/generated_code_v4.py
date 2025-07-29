from classiq import *

@qfunc
def main(q: Output[QArray[QBit]]) -> None:
    # Allocate 4 qubits
    allocate(4, q)
    
    # Define the Pauli Hamiltonian H = 0.5XZXX + 0.25YIZI + 0.3XIZY
    # Using modern SparsePauliOp syntax
    hamiltonian = (
        0.5 * Pauli.X(0) * Pauli.Z(1) * Pauli.X(2) * Pauli.X(3) +
        0.25 * Pauli.Y(0) * Pauli.I(1) * Pauli.Z(2) * Pauli.I(3) +
        0.3 * Pauli.X(0) * Pauli.I(1) * Pauli.Z(2) * Pauli.Y(3)
    )
    
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
print(f"Number of qubits: {qprog.data.width}")
print("Hamiltonian evolution with Suzuki-Trotter completed.")

# Show the circuit
show(qprog)