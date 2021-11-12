import numpy as np
import matplotlib.pyplot as plt
from hebb.util import *

q = 0.5
dt = 0.1
N = 20000
Nrecord = 1000
T = 5000
Nt = int(round(T/dt))
N_e = int(round(q*N))
N_i = int(round((1-q)*N))
N_e1 = int(round(N_e/2))
N_i1 = int(round(N_i/2))


pee0 = 0.25
pei0 = 0.25
pie0 = 0.25
pii0 = 0.25

jee = 12.5
jei = 50
jie = 20
jii = 50

wee0 = jee*pee0*q
wei0 = jei*pei0*(1-q)
wie0 = jie*pie0*q
wii0 = jii*pii0*(1-q)

Kee = pee0*N_e
Kei = pei0*N_e
Kie = pie0*N_i
Kii = pii0*N_i

taux = 40
mxe = 0.015*np.sqrt(N)
mxi = 0.01*np.sqrt(N)
vxe = 0.05
vxi = 0.05

mxe0=(mxe/np.sqrt(N))
mxi0=(mxi/np.sqrt(N))

tausyne = 8.0
tausyni = 4.0
tausynx = 12.0

Jee=jee/np.sqrt(N)
Jei=-jei/np.sqrt(N)
Jie=jie/np.sqrt(N)
Jii=-jii/np.sqrt(N)

maxns = N*T*0.02

gl = [1/15, 1/10]
Cm = [1.0, 1.0]
vlb = [-100.0, -100.0]
vth = [-10.0, -10.0]
vl = [-60.0, -60.0]
DeltaT = [2.0, 0.5]
vT = [-50.0, -50.0]
vre = [-65.0, -65.0]
tref = [1.5, 0.5]

v0min=vre[1]
v0max=vT[1]
v0 = np.random.uniform(v0min, v0max, size=(N,))
v0 = list(v0)
v0 = [x.item() for x in v0]

print(f'\nThis list should be decreasing for a balanced state to exist: {mxe0/mxi0},{wei0/wii0},{wee0/wie0}\n')
print(f'Also, this number should be greater than 1: {wii0/wee0}\n')
print(f'E Rate: {(mxe0*wii0-mxi0*wei0)/(wei0*wie0-wee0*wii0)} \n ')
print(f'I Rate {(mxe0*wii0-mxi0*wei0)/(wei0*wie0-wee0*wii0)}')


trials = 1

rnn = ExInEIF(N,trials,Nrecord,T,Nt,N_e,N_i,q,dt,pee0,pei0,pie0,pii0,jee,jei,
              jie,jii,wee0,wei0,wie0,wii0,Kee,Kei,Kie,Kii,taux,tausyne,tausyni,
              tausynx,Jee,Jei,Jie,Jii,maxns,gl,Cm,vlb,vth,DeltaT,vT,vl,vre,tref,
              mxe, mxi, vxe, vxi)

rnn.call(v0)
fig_7(rnn)
plt.show()
