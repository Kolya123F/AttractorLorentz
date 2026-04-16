import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def f1(nu, alpha, omega, A, x, v, t):
    return v

def f2(nu, alpha, omega, A, x, v, t):
    return nu * (1 - x ** 2) * v - x - alpha * x ** 3 + np.cos(omega * t)

def f(nu, alpha, omega, A, x, v, t):
    return np.array([f1(nu, alpha, omega, A, x, v, t), f2(nu, alpha, omega, A, x, v, t)])

#Начальное условие
x_0 = 2
v_0 = 0

#Число точек
number = 50000

#Длительность
T = 100

#Параметры системы
nu = 1
alpha = 0.1
omega = 5
A = 1

#Решаем численно систему диффуром методом Рунге-Кутта
def solve(x_0, v_0, nu, alpha, omega, A, number, T):
    t = np.linspace(0, T, number)
    h = t[1] - t[0]
    sol = np.zeros((2, number))
    sol[0, 0] = x_0
    sol[1, 0] = v_0
    for i in range(0, number - 1):
        ti = t[i]
        xi, vi = sol[:, i]
        k_1 = f(nu, alpha, omega, A, xi, vi, ti)
        k_2 = f(nu, alpha, omega, A, xi + h * k_1[0]/2, vi + h * k_1[1]/2, ti)
        k_3 = f(nu, alpha, omega, A, xi + h * k_2[0]/2, vi + h * k_2[1]/2, ti)
        k_4 = f(nu, alpha, omega, A, xi + h * k_3[0], vi + h * k_3[1], ti)
        sol[:, i + 1] = sol[:, i] + h * (k_1 + 2 * k_2 + 2 * k_3 + k_4)/6
    x = sol[0, :]
    v = sol[1, :]

    return t, x, v

t, x, v = solve(x_0, v_0, nu, alpha, omega, A, number, T)

r_vals = np.arange(0.1, 15, 0.1)

x_max = []
for r in r_vals:
    t, x, v = solve(x_0, v_0, r, alpha, omega, A, number, T)
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
#plt.title('Бифуркационная диаграмма аттрактора Лоренца')
plt.show()