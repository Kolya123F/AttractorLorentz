import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def f1(nu, alpha, omega, A, x, v, t):
    return v

def f2(nu, alpha, omega, A, x, v, t):
    return nu * (1 - x ** 2) * v - x - alpha * x ** 3 + A * np.cos(omega * t)

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
nu = 0.2
alpha = 0.1
omega = 2
A = 2

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

fig, ax = plt.subplots(figsize=(10, 10))

ax.set_xlabel('x')
ax.set_ylabel('v')

lim_min_x = np.min([np.min(x)])
lim_max_x = np.min([np.max(x)])

lim_min_v = np.max([np.min(v)])
lim_max_v = np.max([np.max(v)])

ax.set_ylim([lim_min_v, lim_max_v])
ax.set_xlim([lim_min_x, lim_max_x])

animated_line, = ax.plot([], [], linewidth=0.5, linestyle='--', color='blue')

point, = ax.plot([], [], 'bo', markersize=3)

def update(frame):
    animated_line.set_data(x[:frame], v[:frame])
    
    point.set_data([x[frame]], [v[frame]])
    
    #ax.set_title(f'Аттрактор Лоренца: $\sigma = 10 \\text{{, }} r = 28 \\text{{, }} b = 8/3$\nВремя: {t[frame]:.2f} из {t[-1]:.1f}')
    
    return animated_line, point

animation = FuncAnimation(
    fig=fig, 
    func=update, 
    frames=range(0, number, 30), 
    interval=20,  # Интервал между кадрами в мс
    blit=True,   # blit=True может вызвать проблемы в 3D, оставляем False
    repeat=False   # Зациклить анимацию
)

#animation.save('lorenz_attractor.gif', writer='pillow', fps=60)  # Для GIF
#animation.save('lorenz_attractor.mp4', writer='ffmpeg', fps=30)  # Для MP4
ax.legend()
ax.grid()
plt.show()