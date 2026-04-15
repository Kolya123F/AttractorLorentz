import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

x0 = 1
y0 = 1
z0 = 1

number = 10000

x = np.zeros(number)
y = np.zeros(number)
z = np.zeros(number)

sol = np.vstack([x, y, z])

t = np.linspace(0, 100, number)

def f1(x, y, z):
    return - y - z

def f2(a, x, y, z):
    return x + a * y

def f3(b, c, x, y, z):
    return b + z * (x - c)

def f(a, b, c, x, y, z):
    return np.array([f1(x, y, z), f2(a, x, y, z), f3(b, c, x, y, z)])

a, b, c = 0.2, 0.2, 5.7
h = t[1] - t[0]

x[0], y[0], z[0] = x0, y0, z0

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

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot([x0], [y0], [z0], 'bo', markersize=3)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.set_xlim([np.min(x), np.max(x)])
ax.set_ylim([np.min(y), np.max(y)])
ax.set_zlim([np.min(z), np.max(z)])

animated_line, = ax.plot([], [], [], linewidth=0.5, color='blue')

point, = ax.plot([], [], [], 'ro', markersize=3)

def update(frame):
    animated_line.set_data(x[:frame], y[:frame])
    animated_line.set_3d_properties(z[:frame])
    
    point.set_data([x[frame]], [y[frame]])
    point.set_3d_properties([z[frame]])

    ax.set_title(f'Аттрактор Ресслера\nВремя: {t[frame]:.2f} из {t[-1]:.1f}')
    
    return animated_line, point

animation = FuncAnimation(
    fig=fig, 
    func=update, 
    frames=range(0, number, 25), 
    interval=20,  # Интервал между кадрами в мс
    blit=False,   # blit=True может вызвать проблемы в 3D, оставляем False
    repeat=True   # Зациклить анимацию
)

# Сохранение (раскомментируйте нужную строку)
#animation.save('lorenz_attractor.gif', writer='pillow', fps=60)  # Для GIF
#animation.save('lorenz_attractor.mp4', writer='ffmpeg', fps=30)  # Для MP4
plt.show()