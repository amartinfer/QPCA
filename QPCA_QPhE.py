from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np
from qiskit import BasicAer, execute
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
import cmath

q=QuantumRegister(4)
c=ClassicalRegister(4)
qc=QuantumCircuit(q,c)

#initial state of the fourth qubit (eigenstate)
phase0=complex(math.cos(-0.1144),math.sin(-0.1144))
phase1=complex(math.cos(0.3252-0.1144),math.sin(0.3252-0.1144))
state_vector=[math.cos(0.4996)*phase0,math.sin(0.4996)*phase1]
qc.initialize(state_vector,[q[3]])
#preparation of the three first qubits (3-bit eigenvalue estimation)
qc.h(q[0])
qc.h(q[1])
qc.h(q[2])

#Controlled U_rho
qc.cu3(1.59899,-1.11512,2.02647,q[2],q[3])

#Controlled U_rho^2
qc.cu3(2.22862,0.513123,3.65472,q[1],q[3])

#Controlled U_rho^4
qc.cu3(0.797922,-4.53103,-1.38944,q[0],q[3])

#Inverse QFT
qc.h(q[0])
qc.cu1(-1/2*np.pi,q[0],q[1])
qc.h(q[1])
qc.cu1(-1/4*np.pi,q[0],q[2])
qc.cu1(-1/2*np.pi,q[1],q[2])
qc.h(q[2])

#Run on Statevector smulator
backend_state=BasicAer.get_backend('statevector_simulator')
job_state=execute(qc,backend_state)
result_state=job_state.result()
outputstate=result_state.get_statevector(qc,decimals=3)
print(outputstate)

#projection and meassurement
qc.barrier(q[0])
qc.barrier(q[1])
qc.barrier(q[3])
qc.measure(q[0],c[0])
qc.measure(q[1],c[1])
qc.measure(q[2],c[2])
qc.measure(q[3],c[3])
qc.draw(output='mpl')

#Run on qasm simulator
backend_qasm=BasicAer.get_backend('qasm_simulator')
job_qasm=execute(qc,backend_qasm,shots=8192)
result_qasm=job_qasm.result()
counts=result_qasm.get_counts(qc)
print(counts)
plot_histogram(counts)
sim_jobID=job_qasm.job_id()
print('SIMULATION JOB ID: {}'.format(sim_jobID)) 

#Run on real device
backend_exp=IBMQ.get_backend('ibmqx2')
backend_exp.name()
job_exp=execute(qc,backend_exp,shots=8192)#,max_credits=3)
job_monitor(job_exp)
result_exp=job_exp.result()
counts_exp = result_exp.get_counts()
print(counts_exp)
plot_histogram([counts_exp,counts])
jobID=job_exp.job_id()
print('JOB ID: {}'.format(jobID))