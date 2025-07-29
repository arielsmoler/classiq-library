import time
from classiq import *
from classiq.execution import ExecutionPreferences

def run_test():
    start_time = time.time()
    
    # Define the Hamiltonian terms
    # H = 0.5XZXX + 0.25YIZI + 0.3XIZY
    
    # Create Pauli terms for the Hamiltonian
    pauli_terms = [
        PauliTerm(pauli=[Pauli.X, Pauli.Z, Pauli.X, Pauli.X], coefficient=0.5),
        PauliTerm(pauli=[Pauli.Y, Pauli.I, Pauli.Z, Pauli.I], coefficient=0.25),
        PauliTerm(pauli=[Pauli.X, Pauli.I, Pauli.Z, Pauli.Y], coefficient=0.3)
    ]
    
    # Create the quantum model with 4 qubits
    @qfunc
    def main():
        qubits = QArray("qubits")
        allocate(4, qubits)
        
        # Apply Suzuki-Trotter evolution
        suzuki_trotter(
            pauli_operator=pauli_terms,
            evolution_coefficient=3.0,
            order=2,
            repetitions=4,
            qbv=qubits
        )
    
    model = create_model(main)
    
    print("Model created successfully")
    
    # Synthesize the circuit
    quantum_program = synthesize(model)
    
    print("Synthesis completed successfully")
    
    # Show circuit information
    print(f"\nCircuit Information:")
    print(f"Number of qubits: {quantum_program.data.width}")
    
    # Execute the circuit
    job = execute(quantum_program)
    results = job.result()
    
    print(f"\n=== Hamiltonian Evolution Results ===")
    print(f"Counts: {results[0].value.counts}")
    
    generation_time = time.time() - start_time
    print(f"\nGeneration time: {generation_time:.3f} seconds")

if __name__ == "__main__":
    run_test()
