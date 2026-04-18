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

#Число точек
number = 100000

#Начальные условия
x_01 = 1
y_01 = 1
z_01 = 1

x_02 = 1 + 0.00001
y_02 = 1
z_02 = 1

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
        k_2 = f(sigma, r, b, xi + h * k_1[0]/2, yi + h * k_1[1]/2, 
                zi + h * k_1[2]/2)
        k_3 = f(sigma, r, b, xi + h * k_2[0]/2, yi + h * k_2[1]/2, 
                zi + h * k_2[2]/2)
        k_4 = f(sigma, r, b, xi + h * k_3[0], yi + h * k_3[1], 
                zi + h * k_3[2])
        sol[:, i + 1] = sol[:, i] + h * (k_1 + 2 * k_2 + 2 * k_3 + k_4)/6
    x = sol[0, :]
    y = sol[1, :]
    z = sol[2, :]

    return t, x, y, z

#Решения с разными начальными условиями 
t, x1, y1, z1 = solve(sigma, r, b, x_01, y_01, z_01, number, T)
t, x2, y2, z2 = solve(sigma, r, b, x_02, y_02, z_02, number, T)

#Создаем область для отрисовки графиков
fig = plt.figure(figsize=(10, 8))

ax = fig.add_subplot(121, projection='3d')
ax1 = fig.add_subplot(122)

#Обзываем оси для фазовой кривой в 3D 
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

#Обзываем оси для временной зависимости расстояния между решениями
ax1.set_xlabel('t')
ax1.set_ylabel('dist')

#Расстояние между решениями
dist = np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2 + (z1 - z2) ** 2)

#Устанавливаем границы для графиков
ax.set_xlim([np.min(x1), np.max(x1)])
ax.set_ylim([np.min(y1), np.max(y1)])
ax.set_zlim([np.min(z1), np.max(z1)])

ax1.set_xlim([0, T])
ax1.set_ylim([-1, np.max(dist)])

animated_line_1, = ax.plot([], [], [], linewidth=0.5, linestyle='--', 
                           color='blue', 
                           label = (r'$x_0 = 1'
                                    r' \text{, } y_0 = 1 \text{, } z_0 = 1$'))
point_1, = ax.plot([], [], [], 'bo', markersize=3)

animated_line_2, = ax.plot([], [], [], linewidth=0.5, linestyle='-', 
                           color='green', 
                           label = (r'$x_0 = 1 + 10^{-5}'  
                                    r'\text{, } y_0 = 1 \text{, } z_0 = 1$'))
point_2, = ax.plot([], [], [], 'go', markersize=3)

animated_line, = ax1.plot([], [], linewidth=0.5, linestyle='-', color='black')

#Точки равновесия
x_pos_1 = round(np.sqrt(b * (r - 1)), 2)
y_pos_1 = x_pos_1
z_pos_1 = r - 1

x_pos_2 = -round(np.sqrt(b * (r - 1)), 2)
y_pos_2 = x_pos_2
z_pos_2 = r - 1

equilibrium_positiona_1 = ax.plot([x_pos_1], [y_pos_1], [z_pos_1], 'o', 
                                  color = 'black', markersize=4, 
                                  label = f'{(x_pos_1, y_pos_1, z_pos_1)}')

equilibrium_positiona_2 = ax.plot([x_pos_2], [y_pos_2], [z_pos_2], 'o', 
                                  color = 'gray', markersize=4, 
                                  label = f'{(x_pos_2, y_pos_2, z_pos_2)}')

def update(frame):
    animated_line_1.set_data(x1[:frame], y1[:frame])
    animated_line_1.set_3d_properties(z1[:frame])
    point_1.set_data([x1[frame]], [y1[frame]])
    point_1.set_3d_properties([z1[frame]])

    animated_line_2.set_data(x2[:frame], y2[:frame])
    animated_line_2.set_3d_properties(z2[:frame])
    point_2.set_data([x2[frame]], [y2[frame]])
    point_2.set_3d_properties([z2[frame]])

    animated_line.set_data(t[:frame], dist[:frame])
    ax.set_title(f'Аттрактор Лоренца:\n'
                f'$\sigma = 10 \\text{{, }}$'
                f'$r = 28 \\text{{, }}$'
                f'$b = 8/3$\n'
                f'Шаг дискретизации: ${dt}$\n'
                f'Время: {t[frame]:.2f} из {t[-1]:.1f}')
    return animated_line_1, point_1, animated_line_2, point_2, animated_line

animation = FuncAnimation(
    fig=fig, 
    func=update, 
    frames=range(0, number, 1000), 
    interval=20,  # Интервал между кадрами в мс
    blit=False,   # blit=True может вызвать проблемы в 3D, оставляем False
    repeat=False   # Зациклить анимацию
)

#animation.save('lorenz_attractor.gif', writer='pillow', fps=30)  # Для GIF
#animation.save('lorenz_attractor.mp4', writer='ffmpeg', fps=30)  # Для MP4
ax.legend()
ax1.grid()
plt.show()
