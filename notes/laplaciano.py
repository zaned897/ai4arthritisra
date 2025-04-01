"""Script to estimate the Laplacian Operator using discrete maths"""
#%%
import numpy as np
from matplotlib import pyplot as plt

# Gradient
x = np.linspace(-3, 3, 300)
y = np.linspace(-3, 3, 300)
X, Y = np.meshgrid(x, y)
phi = X**2 + Y**2
h = 0.01
grad_x = (phi[1:-1, 2:] - phi[1:-1, :-2]) / 2*h
grad_y = (phi[2:, 1:-1] - phi[:-2, 1:-1]) / 2*h

#%%
plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
plt.contourf(X, Y, phi, cmap='viridis')
plt.title('Función Escalar φ(x,y)')

plt.subplot(1, 2, 2)
plt.quiver(X[1:-1, 1:-1], Y[1:-1, 1:-1], grad_x, grad_y, scale=30, color='red')
plt.title('Gradiente ∇φ')
#%%