#Импорт необходимых библиотек
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

#Правая часть системы диффуров
def f1(sigma, x, y):
    return sigma * (y - x)

def f2(r, x, y, z):
    return x * (r - z) - y

def f3(b, x, y, z):
    return x * y - b * z

def f(sigma, r, b, x, y, z):
    return np.array([f1(sigma, x, y), f2(r, x, y, z), f3(b, x, y, z)])

#Параметры системы
sigma, r, b = 10, 28, 8/3

#Начальные условия
x_0 = 1
y_0 = 1
z_0 = 1

#Число точек
number = 100000

#Длительность
T = 30

#Шаг дискретизации
dt = T / number 

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

#Решаем систему
t, x, y, z = solve(sigma, r, b, x_0, y_0, z_0, number, T)

#Создаем область для отрисовки графика
fig, ax = plt.subplots(2, 1, figsize=(10, 10))

#Обзываем оси
ax[0].set_xlabel('t')
ax[0].set_ylabel('x, y, z')

#Устанавливаем границы
lim_min = np.min([np.min(x), np.min(y), np.min(z)])
lim_max = np.max([np.max(x), np.max(y), np.max(z)])

ax[0].set_ylim([lim_min, lim_max])
ax[0].set_xlim([0, T])

#Точки равновесия
x_pos_1 = round(np.sqrt(b * (r - 1)), 2)
y_pos_1 = x_pos_1
z_pos_1 = r - 1

x_pos_2 = -round(np.sqrt(b * (r - 1)), 2)
y_pos_2 = x_pos_2
z_pos_2 = r - 1

ax[0].plot(t, [x_pos_2] * len(t), linewidth=0.5, linestyle='--')
ax[0].plot(t, [z_pos_2] * len(t), linewidth=0.5, linestyle='--')

#Создаем анимацию фазовой кривой
animated_line_1, = ax[0].plot([], [], linewidth=0.5, 
                              linestyle='-', color='blue', label = '$x(t)$')
point_1, = ax[0].plot([], [], 'bo', markersize=3)

animated_line_2, = ax[0].plot([], [], linewidth=0.5, 
                              linestyle='-', color='green', label = '$y(t)$')
point_2, = ax[0].plot([], [], 'go', markersize=3)

animated_line_3, = ax[0].plot([], [], linewidth=0.5, 
                              linestyle='-', color='red', label = '$z(t)$')
point_3, = ax[0].plot([], [], 'ro', markersize=3)

#Фурье-преобразование (метод FFT) от x(t), y(t), z(t)
fourier_x = np.fft.fft(x, axis = 0)
amplitude_spectrum_x = np.abs(fourier_x)
frequencies_x = np.fft.fftfreq(len(x), t[1] - t[0])

fourier_y = np.fft.fft(y, axis = 0)
amplitude_spectrum_y = np.abs(fourier_y)
frequencies_y = np.fft.fftfreq(len(y), t[1] - t[0])

fourier_z = np.fft.fft(z, axis = 0)
amplitude_spectrum_z = np.abs(fourier_z)
frequencies_z = np.fft.fftfreq(len(z), t[1] - t[0])

def update(frame):
    animated_line_1.set_data(t[:frame], x[:frame])
    point_1.set_data([t[frame]], [x[frame]])

    animated_line_2.set_data(t[:frame], y[:frame])
    point_2.set_data([t[frame]], [y[frame]])

    animated_line_3.set_data(t[:frame], z[:frame])
    point_3.set_data([t[frame]], [z[frame]])
    
    ax[0].set_title(f'Аттрактор Лоренца:\n'
                    f'$\sigma = 10 \\text{{, }}$'
                    f'$r = 28 \\text{{, }}$'
                    f'$b = 8/3$\n'
                    f'Шаг дискретизации: ${dt}$\n'
                    f'Время: {t[frame]:.2f} из {t[-1]:.1f}')
    
    return (
        animated_line_1, point_1, 
        animated_line_2, point_2, 
        animated_line_3, point_3
        )

animation = FuncAnimation(
    fig=fig, 
    func=update, 
    frames=range(0, number, 1000), 
    interval=20,  # Интервал между кадрами в мс
    blit=False,   # blit=True может вызвать проблемы в 3D, оставляем False
    repeat=False   # Зациклить анимацию
)

#animation.save('lorenz_attractor.gif', writer='pillow', fps=60)  # Для GIF
#animation.save('lorenz_attractor.mp4', writer='ffmpeg', fps=30)  # Для MP4

#Отрисовываем фурье-спектры
ax[1].plot(frequencies_x, amplitude_spectrum_x, 'b-', 
           alpha=0.7, label='Преобразование Фурье от x(t)', linewidth=1)
ax[1].plot(frequencies_y, amplitude_spectrum_y, 'g-', 
           alpha=0.7, label='Преобразование Фурье от y(t)', linewidth=0.5)
ax[1].plot(frequencies_z, amplitude_spectrum_z, 'r-', 
           alpha=0.7, label='Преобразование Фурье от z(t)', linewidth=0.25)

#Лог. масштаб по осям Y и X  для фурье-спектра
ax[1].set_yscale('log')
ax[1].set_xscale('log')

#Обзываем график фурье-спектров
ax[1].set_title('Фурье-спектр временных зависимостей координат')

#Обзываем оси для фурье-спектра
ax[1].set_xlabel('$\omega$')
ax[1].set_ylabel('$A$')

ax[1].legend()
ax[1].grid()

ax[0].legend()
ax[0].grid()
plt.show()