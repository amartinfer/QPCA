
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np
from qiskit import BasicAer, execute
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
import math

q=QuantumRegister(3)
c=ClassicalRegister(3)
qc=QuantumCircuit(q,c)

#initial state of the third qubit (eigenstate)
state_vector=[1/math.sqrt(2),1/math.sqrt(2)]
qc.initialize(state_vector,[q[2]])
#preparation of the two first qubits (2-bit eigenvalue estimation)
qc.h(q[0])
qc.h(q[1])

#Controlled U_rho
qc.cu3(1.59899,-1.11512,2.02647,q[1],q[2])

#Controlled U_rho^2
qc.cu3(2.22862,0.513123,3.65472,q[0],q[2])

#Inverse QFT
qc.h(q[0])
qc.cu1(-1/2*np.pi,q[0],q[1])
qc.h(q[1])

##measure on X basis
#qc.h(q[3])

##measure on Y basis
#qc.h(q[3])
#qc.u1(1/2*np.pi,q[3])

##measure on Random basis
#qc.u3(2*0.4987,0.9876,0.9876,q[2])

#Run on Statevector smulator
backend_state=BasicAer.get_backend('statevector_simulator')
job_state=execute(qc,backend_state)
result_state=job_state.result()
outputstate=result_state.get_statevector(qc,decimals=3)
print(outputstate)

#projection and meassurement
qc.barrier(q[0])
qc.barrier(q[1])
qc.measure(q[0],c[0])
qc.measure(q[1],c[1])
qc.measure(q[2],c[2])
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
print('REAL CHIP JOB ID: {}'.format(jobID)) 