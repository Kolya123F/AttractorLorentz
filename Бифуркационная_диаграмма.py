import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

#Правая часть системы диффуров
def f1(sigma, x, y, z):
    return sigma * (y - x)

def f2(r, x, y, z):
    return x * (r - z) - y

def f3(b, x, y, z):
    return x * y - b * z

def f(sigma, r, b, x, y, z):
    return np.array([f1(sigma, x, y, z), f2(r, x, y, z), f3(b, x, y, z)])

#Начальные условия
x_0 = 1
y_0 = 1
z_0 = 1

#Число точек
number = 5000

#Длительность
T = 100

#Параметры системы
sigma, r, b = 10, 30, 8/3

#Решаем численно систему диффуром методом Рунге-Кутта
def solve(sigma, r, b, x0, y0, z0, number, T):
    t = np.linspace(0, T, number)
    h = t[1] - t[0]
    sol = np.zeros((3, number))
    sol[0, 0] = x0
    sol[1, 0] = y0
    sol[2, 0] = z0
    for i in range(0, number - 1):
        xi, yi, zi = sol[:, i]
        k_1 = f(sigma, r, b, xi, yi, zi)
        k_2 = f(sigma, r, b, xi + h * k_1[0]/2, yi + h * k_1[1]/2, zi + h * k_1[2]/2)
        k_3 = f(sigma, r, b, xi + h * k_2[0]/2, yi + h * k_2[1]/2, zi + h * k_2[2]/2)
        k_4 = f(sigma, r, b, xi + h * k_3[0], yi + h * k_3[1], zi + h * k_3[2])
        sol[:, i + 1] = sol[:, i] + h * (k_1 + 2 * k_2 + 2 * k_3 + k_4)/6
    x = sol[0, :]
    y = sol[1, :]
    z = sol[2, :]

    return t, x, y, z

r_vals = np.arange(23.77, 23.81, 0.00001)

x_max = []
for r in r_vals:
    t, x, y, z = solve(sigma, r, b, x_0, y_0, z_0, number, T)
    x = x[2500:]
    x_r_max = []
    for i in range(1, len(x) - 1):
        if x[i - 1] < x[i] > x[i + 1]:
            x_r_max.append(x[i])
    x_max.append(x_r_max)

plt.figure()
for r, max in zip(r_vals, x_max):
    plt.scatter([r]*len(max), max, s=0.5, color='black', alpha=0.3)
plt.xlabel('r')
plt.ylabel('Максимумы x')
plt.title('Бифуркационная диаграмма аттрактора Лоренца')
plt.show()