import numpy as np
from matplotlib import pyplot as plt

T = 2.0
L = 2.0

dt = 0.01
dx = 0.1

nx = int(L / dx + 1)
nt = int(T / dt + 1)

c = 1.0

x = np.linspace(0, L, nx)

u0 = np.ones(nx)
mask = np.where(np.logical_and(x >= 0.5, x <= 1.0))
u0[mask] = 2.0

#u0 = np.sin(x)

u = np.zeros((nt, nx))
u[0, :] = u0
for n in range(1, nt):
    for i in range(1, nx):
        u[n, i] = u[n - 1, i] - u[n - 1, i] * dt / dx * (u[n - 1, i] - u[n - 1, i - 1])

plt.figure(figsize=(4.0, 4.0))
plt.xlabel('x')
plt.ylabel('u')
plt.grid()
plt.plot(x, u0, label='Initial', color='C0', linestyle='--', linewidth=2)
plt.plot(x, u[25, :], label='nt = {}'.format(nt), color='C1', linestyle='-', linewidth=2)
plt.legend()
plt.xlim(0.0, L)
plt.ylim(0, 2.5)
plt.show()

