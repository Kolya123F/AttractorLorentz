import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider

def solve_osc_graph(omega, beta, q, r, dt, T):
    tt, y = solve_osc(omega = 10, beta = 1000, q = 1, r = 0, dt = 0.0001, T = 10)
    
    plt.figure(figsize=(8, 4))
    plt.plot(tt, y[0, :], 'b-', linewidth=2)
    plt.grid(True, alpha=0.3)
    #plt.title(f'График sin({a}·x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.ylim(-1.5, 1.5)
    plt.show()

# Создаем ползунок для параметра a
interact(solve_osc_graph, omega = FloatSlider(min=0.1, max=5, step=0.1, value=1), beta = FloatSlider(min=0.1, max=10, step=0.1, value=1),
        q = FloatSlider(min=0.1, max=5, step=0.1, value=1), r = FloatSlider(min=0.1, max=5, step=0.1, value=1), 
        dt = FloatSlider(min=0.1, max=5, step=0.1, value=1), T = FloatSlider(min=0.1, max=5, step=0.1, value=1))