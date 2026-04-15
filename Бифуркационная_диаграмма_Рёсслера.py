import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

#Правая часть системы диффуров
def f1(x, y, z):
    return -y - z

def f2(a, x, y, z):
    return x + a * y

def f3(b, c, x, y, z):
    return b + z * (x - c)

def f(a, b, c, x, y, z):
    return np.array([f1(x, y, z), f2(a, x, y, z), f3(b, c, x, y, z)])

#Начальные условия
x_0 = 1
y_0 = 1
z_0 = 1

#Число точек
number = 5000

#Длительность
T = 100

#Параметры системы
a, b, c = 0.2, 0.2, 5.7

#Решаем численно систему диффуром методом Рунге-Кутта
def solve(a, b, c, x0, y0, z0, number, T):
    t = np.linspace(0, T, number)
    h = t[1] - t[0]
    sol = np.zeros((3, number))
    sol[0, 0] = x0
    sol[1, 0] = y0
    sol[2, 0] = z0
    for i in range(0, number - 1):
        xi, yi, zi = sol[:, i]
        k_1 = f(a, b, c, xi, yi, zi)
        k_2 = f(a, b, c, xi + h * k_1[0]/2, yi + h * k_1[1]/2, zi + h * k_1[2]/2)
        k_3 = f(a, b, c, xi + h * k_2[0]/2, yi + h * k_2[1]/2, zi + h * k_2[2]/2)
        k_4 = f(a, b, c, xi + h * k_3[0], yi + h * k_3[1], zi + h * k_3[2])
        sol[:, i + 1] = sol[:, i] + h * (k_1 + 2 * k_2 + 2 * k_3 + k_4)/6
    x = sol[0, :]
    y = sol[1, :]
    z = sol[2, :]

    return t, x, y, z

b_vals = np.arange(0.001, 2, 0.001)
x_max = []
for b_val in b_vals:
    t, x, y, z = solve(a, b_val, c, x_0, y_0, z_0, number, T)
    x = x[2500:]
    x_r_max = []
    for i in range(1, len(x) - 1):
        if x[i - 1] < x[i] > x[i + 1]:
            x_r_max.append(x[i])
    x_max.append(x_r_max)

plt.figure()
for r, max in zip(b_vals, x_max):
    plt.scatter([r]*len(max), max, s=0.5, color='black', alpha=0.3)
plt.xlabel('r')
plt.ylabel('Максимумы x')
plt.title('Бифуркационная диаграмма аттрактора Рёсслера')
plt.grid()
plt.show()