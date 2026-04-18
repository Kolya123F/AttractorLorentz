import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider

def solve_osc(omega, beta, q, r, dt, T):
    u0 = np.asarray([q, r], dtype=float)
    num_steps = int(T/dt)
    tt = np.arange(num_steps+1)*dt
    u = np.empty((2, num_steps+1))
    u[:, 0] = u0
    
    for k in range(num_steps):
        # Сначала вычисляем новую скорость
        u[1, k+1] = (-omega**2 * u[0, k] - beta * u[0, k]**3) * dt + u[1, k]
        # Затем новую позицию
        u[0, k+1] = u[1, k] * dt + u[0, k]
    
    return tt, u

def solve_osc_graph(omega, beta, q, r, dt, T):
    # Используем переданные параметры
    tt, y = solve_osc(omega, beta, q, r, dt, T)
    
    plt.figure(figsize=(10, 6))
    plt.plot(tt, y[0, :], 'b-', linewidth=2, label='Позиция')
    plt.plot(tt, y[1, :], 'r-', linewidth=1, alpha=0.7, label='Скорость')
    plt.grid(True, alpha=0.3)
    plt.title(f'Осциллятор (ω={omega}, β={beta})')
    plt.xlabel('Время t')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.ylim(-2, 2)
    plt.show()
    print(f"dt = {dt}, T = {T}, шагов = {int(T/dt)}")

# Создаем ползунки
interact(solve_osc_graph, 
         omega=FloatSlider(min=0.1, max=20, step=0.5, value=10, description='ω'),
         beta=FloatSlider(min=0, max=2000, step=50, value=1000, description='β'),
         q=FloatSlider(min=-2, max=2, step=0.1, value=1, description='q(0)'),
         r=FloatSlider(min=-5, max=5, step=0.5, value=0, description='r(0)'),
         dt=FloatSlider(min=0.0001, max=0.01, step=0.0001, value=0.001, description='dt'),
         T=FloatSlider(min=1, max=20, step=1, value=10, description='T'))