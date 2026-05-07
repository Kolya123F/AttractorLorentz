# Lorenz Attractor Simulation

Численное исследование системы Лоренца с использованием метода Рунге–Кутты 4 порядка.

Проект включает:
- построение аттрактора Лоренца,
- анализ чувствительности к начальным условиям,
- FFT-анализ,
- построение бифуркационной диаграммы.

## Mathematical Model

The Lorenz system:

$$
\dot{x} = \sigma(y - x)
$$

$$
\dot{y} = x(r - z) - y
$$

$$
\dot{z} = xy - bz
$$

Parameters used in the project:

- $\sigma = 10$
- $r = 28$
- $b = 8/3$

![Lorenz attractor](Картинки+видео/lorenz_attractor.gif)