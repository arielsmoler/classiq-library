from classiq import *
from classiq.qmod.hamiltonian import PauliTerm
import numpy as np

@qfunc
def main(q: QArray[QBit]):
    # Define the Pauli Hamiltonian H = 0.5XZXX + 0.25YIZI + 0.3XIZY
    # Each term is defined as coefficient and Pauli string
    hamiltonian = [
        PauliTerm(pauli=[Pauli.X, Pauli.Z, Pauli.X, Pauli.X], coefficient=0.5),
        PauliTerm(pauli=[Pauli.Y, Pauli.I, Pauli.Z, Pauli.I], coefficient=0.25),
        PauliTerm(pauli=[Pauli.X, Pauli.I, Pauli.Z, Pauli.Y], coefficient=0.3)
    ]
    
    # Apply Suzuki-Trotter evolution
    suzuki_trotter(
        hamiltonian=hamiltonian,
        evolution_coefficient=3,
        repetitions=4,
        order=2,
        qbv=q
    )

# Create the quantum model
model = create_model(main)

# Set execution preferences for 4 qubits
execution_preferences = ExecutionPreferences(
    num_shots=1000
)

# Create quantum program with 4 qubits
qprog = synthesize(model)

print("Circuit synthesized successfully!")
print(f"Circuit depth: {qprog.depth}")
print(f"Number of qubits: {qprog.width}")
print(f"Number of gates: {len(qprog.instructions)}")