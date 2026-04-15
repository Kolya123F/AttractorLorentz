import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

x_01 = 1
y_01 = 1
z_01 = 1

x_02 = 1 + 0.00001
y_02 = 1
z_02 = 1


number = 40000

x1 = np.zeros(number)
y1 = np.zeros(number)
z1 = np.zeros(number)

x2 = np.zeros(number)
y2 = np.zeros(number)
z2 = np.zeros(number)

sol1 = np.vstack([x1, y1, z1])
sol2 = np.vstack([x2, y2, z2])

t = np.linspace(0, 100, number)

def f1(sigma, x, y, z):
    return sigma * (y - x)

def f2(r, x, y, z):
    return x * (r - z) - y

def f3(b, x, y, z):
    return x * y - b * z

def f(sigma, r, b, x, y, z):
    return np.array([f1(sigma, x, y, z), f2(r, x, y, z), f3(b, x, y, z)])

sigma, r, b = 10, 28, 8/3
h = t[1] - t[0]

x1[0], y1[0], z1[0] = x_01, y_01, z_01
x2[0], y2[0], z2[0] = x_02, y_02, z_02

sol1[0, 0] = x_01
sol1[1, 0] = y_01
sol1[2, 0] = z_01

sol2[0, 0] = x_02
sol2[1, 0] = y_02
sol2[2, 0] = z_02


for i in range(0, number - 1):
    xi_1, yi_1, zi_1 = sol1[:, i]
    k_1 = f(sigma, r, b, xi_1, yi_1, zi_1)
    k_2 = f(sigma, r, b, xi_1 + h * k_1[0]/2, yi_1 + h * k_1[1]/2, zi_1 + h * k_1[2]/2)
    k_3 = f(sigma, r, b, xi_1 + h * k_2[0]/2, yi_1 + h * k_2[1]/2, zi_1 + h * k_2[2]/2)
    k_4 = f(sigma, r, b, xi_1 + h * k_3[0], yi_1 + h * k_3[1], zi_1 + h * k_3[2])
    
    sol1[:, i + 1] = sol1[:, i] + h * (k_1 + 2 * k_2 + 2 * k_3 + k_4)/6
    
x1 = sol1[0, :]
y1 = sol1[1, :]
z1 = sol1[2, :]

for i in range(0, number - 1):
    xi_2, yi_2, zi_2 = sol2[:, i]
    k_1 = f(sigma, r, b, xi_2, yi_2, zi_2)
    k_2 = f(sigma, r, b, xi_2 + h * k_1[0]/2, yi_2 + h * k_1[1]/2, zi_2 + h * k_1[2]/2)
    k_3 = f(sigma, r, b, xi_2 + h * k_2[0]/2, yi_2 + h * k_2[1]/2, zi_2 + h * k_2[2]/2)
    k_4 = f(sigma, r, b, xi_2 + h * k_3[0], yi_2 + h * k_3[1], zi_2 + h * k_3[2])
    
    sol2[:, i + 1] = sol2[:, i] + h * (k_1 + 2 * k_2 + 2 * k_3 + k_4)/6
    
x2 = sol2[0, :]
y2 = sol2[1, :]
z2 = sol2[2, :]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.set_xlim([np.min(x1), np.max(x1)])
ax.set_ylim([np.min(y1), np.max(y1)])
ax.set_zlim([np.min(z1), np.max(z1)])

animated_line_1, = ax.plot([], [], [], linewidth=0.5, linestyle='--', color='blue', label = r'$x_0 = 1 \text{, } y_0 = 1 \text{, } z_0 = 1$')
animated_line_2, = ax.plot([], [], [], linewidth=0.5, linestyle='--', color='green', label = r'$x_0 = 1 + 10^{-5}  \text{, } y_0 = 1 \text{, } z_0 = 1$')

point_1, = ax.plot([], [], [], 'bo', markersize=3)
point_2, = ax.plot([], [], [], 'go', markersize=3)

def update(frame):
    animated_line_1.set_data(x1[:frame], y1[:frame])
    animated_line_2.set_data(x2[:frame], y2[:frame])
    animated_line_1.set_3d_properties(z1[:frame])
    animated_line_2.set_3d_properties(z2[:frame])
    
    point_1.set_data([x1[frame]], [y1[frame]])
    point_2.set_data([x2[frame]], [y2[frame]])
    point_1.set_3d_properties([z1[frame]])
    point_2.set_3d_properties([z2[frame]])

    ax.set_title(f'Аттрактор Лоренца: $\sigma = 10 \\text{{, }} r = 28 \\text{{, }} b = 8/3$\nВремя: {t[frame]:.2f} из {t[-1]:.1f}')
    
    return animated_line_1, point_1, animated_line_2, point_2

animation = FuncAnimation(
    fig=fig, 
    func=update, 
    frames=range(0, number, 30), 
    interval=20,  # Интервал между кадрами в мс
    blit=False,   # blit=True может вызвать проблемы в 3D, оставляем False
    repeat=True   # Зациклить анимацию
)

# Сохранение (раскомментируйте нужную строку)
#animation.save('lorenz_attractor.gif', writer='pillow', fps=60)  # Для GIF
plt.legend()
plt.show()
#animation.save('lorenz_attractor.mp4', writer='ffmpeg', fps=30)  # Для MP4
