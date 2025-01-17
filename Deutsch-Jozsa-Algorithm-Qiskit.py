from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram

def create_oracle(n,oracle_type):
    oracle = QuantumCircuit(n+1)
    
    if oracle_type == "balanced": # Creates a balanced state
        for x in range(n):
            oracle.cx(x,n)
    if oracle_type == "constant_zero": # All 0s, initial state
        pass
    if oracle_type == "constant_one": # All 1s, X gate initial state
        oracle.x(n)

    return oracle

# Variables to change #
n = 4 # number of qubits
oracle_type = "balanced" # choices: "balanced", "constant_zero", "constant_one"


oracle = create_oracle(n,oracle_type) # setting up the input to the function
oracle.draw("mpl")





# Setting up our quantum algorithm
qc = QuantumCircuit(n+1,n) # extra classical bit for auxiliary
qc.x(n) # flips auxiliary qubit to |1> (setup)
qc.h(range(n+1)) # Hadamard all qubits


# Inputting oracle
oracle = create_oracle(n,oracle_type)
qc.compose(oracle,inplace=True)

# Processing
qc.h(range(n)) # Hadamard all input gates bar auxiliary

# Measure and print diagram
qc.measure(range(n),range(n))
qc.draw("mpl")





# Simulation
simulator = AerSimulator()
qc_compiled = transpile(qc, simulator)
job = simulator.run(qc_compiled)
result = job.result()

# Data
counts = result.get_counts()
print(f"Results: {counts}")
plot_histogram(counts)
