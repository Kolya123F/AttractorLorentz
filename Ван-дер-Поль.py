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
nu = 8.53
alpha = 0
omega = 2.10
A = 1.2

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

fig, ax = plt.subplots(2, 1, figsize=(10, 10))

ax[0].set_xlabel('t')
ax[0].set_ylabel('x')

lim_min = np.min([np.min(x)])
lim_max = np.max([np.max(x)])

ax[0].set_ylim([lim_min, lim_max])
ax[0].set_xlim([0, T])

animated_line, = ax[0].plot([], [], linewidth=0.5, linestyle='--', color='blue')

point, = ax[0].plot([], [], 'bo', markersize=3)

fourier_x = np.fft.fft(x, axis = 0)

amplitude_spectrum_x = np.abs(fourier_x)

frequencies_x = np.fft.fftfreq(len(x), t[1] - t[0])

def update(frame):
    animated_line.set_data(t[:frame], x[:frame])
    
    point.set_data([t[frame]], [x[frame]])
    
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
ax[1].plot(frequencies_x, amplitude_spectrum_x, 'b-', alpha=0.7, label='Преобразование Фурье от x(t)', linewidth=0.5)
ax[1].set_yscale('log')
ax[1].legend()
ax[1].grid()
ax[0].legend()
ax[0].grid()
plt.show()