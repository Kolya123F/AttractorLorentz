import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

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
number = 40000

#Длительность
T = 100

#Параметры системы
a, b, c = 0.2, 0.2, 3

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

t, x, y, z = solve(a, b, c, x_0, y_0, z_0, number, T)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot()

ax.set_xlabel('t')
ax.set_ylabel('x, y, z')

lim_min = np.min([np.min(x), np.min(y), np.min(z)])
lim_max = np.max([np.max(x), np.max(y), np.max(z)])

ax.set_ylim([lim_min, lim_max])
ax.set_xlim([0, T])

animated_line_1, = ax.plot([], [], linewidth=0.5, linestyle='--', color='blue')
animated_line_2, = ax.plot([], [], linewidth=0.5, linestyle='--', color='green')
animated_line_3, = ax.plot([], [], linewidth=0.5, linestyle='--', color='red')

point_1, = ax.plot([], [], 'bo', markersize=3)
point_2, = ax.plot([], [], 'go', markersize=3)
point_3, = ax.plot([], [], 'ro', markersize=3)

def update(frame):
    animated_line_1.set_data(t[:frame], x[:frame])
    animated_line_2.set_data(t[:frame], y[:frame])
    animated_line_3.set_data(t[:frame], z[:frame])
    
    point_1.set_data([t[frame]], [x[frame]])
    point_2.set_data([t[frame]], [y[frame]])
    point_3.set_data([t[frame]], [z[frame]])
    
    ax.set_title(f'Аттрактор Лоренца: $\sigma = 10 \\text{{, }} r = 28 \\text{{, }} b = 8/3$\nВремя: {t[frame]:.2f} из {t[-1]:.1f}')
    
    return animated_line_1, point_1, animated_line_2, point_2, animated_line_3, point_3

animation = FuncAnimation(
    fig=fig, 
    func=update, 
    frames=range(0, number, 30), 
    interval=20,  # Интервал между кадрами в мс
    blit=False,   # blit=True может вызвать проблемы в 3D, оставляем False
    repeat=True   # Зациклить анимацию
)

#animation.save('lorenz_attractor.gif', writer='pillow', fps=60)  # Для GIF
#animation.save('lorenz_attractor.mp4', writer='ffmpeg', fps=30)  # Для MP4
plt.legend()
plt.grid()
plt.show()