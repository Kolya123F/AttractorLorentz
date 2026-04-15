import matplotlib.pyplot as plt
import numpy as np

# Параметры системы
sigma, r, b = 10, 28, 8/3
x0, y0, z0 = 1, 1, 1

# Временные параметры
number = 50000
t = np.linspace(0, 100, number)
h = t[1] - t[0]

# Функции системы
def f1(sigma, x, y, z):
    return sigma * (y - x)

def f2(r, x, y, z):
    return x * (r - z) - y

def f3(b, x, y, z):
    return x * y - b * z

def f(sigma, r, b, x, y, z):
    return np.array([f1(sigma, x, y, z), f2(r, x, y, z), f3(b, x, y, z)])

# Численное решение
sol = np.zeros((3, number))
sol[0, 0], sol[1, 0], sol[2, 0] = x0, y0, z0

def solve(r):
    for i in range(number - 1):
        xi, yi, zi = sol[:, i]
        k1 = f(sigma, r, b, xi, yi, zi)
        k2 = f(sigma, r, b, xi + h*k1[0]/2, yi + h*k1[1]/2, zi + h*k1[2]/2)
        k3 = f(sigma, r, b, xi + h*k2[0]/2, yi + h*k2[1]/2, zi + h*k2[2]/2)
        k4 = f(sigma, r, b, xi + h*k3[0], yi + h*k3[1], zi + h*k3[2])
        sol[:, i+1] = sol[:, i] + h*(k1 + 2*k2 + 2*k3 + k4)/6
        x_solve, y_solve, z_solve = sol[0, :], sol[1, :], sol[2, :]

    return x_solve, y_solve, z_solve

x, y, z = solve(r)

fig, ax = plt.subplots(1, 1, figsize=(14, 6))

x_extr = []
t_extr = []

for i in range(1, len(x) - 1):
    if x[i-1] < x[i] > x[i+1]:
        x_extr.append(x[i])
        t_extr.append(t[i])

# Левая часть: проекция XY (бабочка)
ax.plot(t, x, linewidth=0.3, color='blue', alpha=0.7, label = 'x')
ax.plot(t, y, linewidth=0.3, color='red', alpha=0.7, label = 'y')
ax.plot(t, z, linewidth=0.3, color='black', alpha=0.7, label = 'z')
plt.scatter(np.array(t_extr), np.array(x_extr), s = 0.5, color='green')

ax.axhline(y=0, color='black', linestyle='--', linewidth=0.5, alpha=0.5)
ax.axvline(x=0, color='black', linestyle='--', linewidth=0.5, alpha=0.5)
ax.set_xlabel('t')
ax.set_ylabel('x, y, z')
ax.set_title('Аттактор Лоренца')
ax.grid(True, alpha=0.3)

ax.legend()
plt.show()
