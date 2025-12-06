import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import os

# --- CONFIGURACIÓN ---
FILE_NAME = 'linearity_data.csv'

# --- GENERACIÓN DE DATOS (Si no hay CSV) ---
if not os.path.exists(FILE_NAME):
    print(f"[!] {FILE_NAME} no encontrado. Simulando datos...")
    steps = np.arange(0, 256, 8) 
    # Añadimos ruido para que la gráfica de residuos sea interesante
    noise = np.random.normal(0, 0.6, len(steps)) 
    measured = (steps * 1.0) + 0.3 + noise
    std_devs = np.abs(np.random.normal(0.2, 0.4, len(steps)))
    
    df = pd.DataFrame({
        'Step': steps,
        'Measured_Mean': measured,
        'Std_Dev': std_devs
    })
else:
    print(f"[OK] Cargando {FILE_NAME}...")
    df = pd.read_csv(FILE_NAME)

# --- CÁLCULOS ---
X = df['Step'].values
Y = df['Measured_Mean'].values

slope, intercept = np.polyfit(X, Y, 1)
Y_pred = slope * X + intercept
r_squared = r2_score(Y, Y_pred)
residuals = Y - Y_pred

# --- ESTILO VISUAL ---
plt.style.use('dark_background')
bg_color = '#0f172a'       # Azul noche profundo
grid_color = '#334155'     # Gris tenue
text_color = '#e2e8f0'     # Blanco hueso

c_line = '#00f2ff'         # Cian Neón (Ideal)
c_dots = '#fbbf24'         # Ámbar (Medido)
c_resid = '#f472b6'        # Rosa (Error)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9), sharex=True, 
                               gridspec_kw={'height_ratios': [3, 1.2], 'hspace': 0.08})
fig.patch.set_facecolor(bg_color)

# === GRÁFICA 1: TRANSFER FUNCTION (Línea + Puntos) ===
ax1.set_facecolor(bg_color)
ax1.set_title("EXPERIMENTO B: LINEALIDAD ESTÁTICA", fontsize=14, fontweight='bold', color='#4ade80', pad=20)

# 1. Línea Ideal (Regreso solicitado)
ax1.plot(X, Y_pred, color=c_line, linewidth=2, alpha=0.5, 
         label=f'Ajuste Ideal ($R^2={r_squared:.5f}$)')

# 2. Puntos Medidos (Encima de la línea)
if 'Std_Dev' in df.columns:
    ax1.errorbar(X, Y, yerr=df['Std_Dev'], fmt='o', 
                 color=c_dots, ecolor='gray', elinewidth=1, capsize=3,
                 markersize=6, markeredgecolor='black', markeredgewidth=0.5, 
                 label='Medición Promedio', zorder=5)
else:
    ax1.scatter(X, Y, color=c_dots, s=50, edgecolor='black', linewidth=0.8, 
                label='Medición Promedio', zorder=5)

# Stats Box
eq_text = (
    f"Model Equation:\n"
    f"$y = {slope:.4f}x + {intercept:.4f}$\n\n"
    f"Linearity Check:\n"
    f"$R^2 = {r_squared:.5f}$\n"
    f"Max Error: {np.max(np.abs(residuals)):.2f} LSB"
)
props = dict(boxstyle='round', facecolor='#1e293b', alpha=0.85, edgecolor=c_line)
ax1.text(0.03, 0.95, eq_text, transform=ax1.transAxes, fontsize=10, 
         verticalalignment='top', bbox=props, color=text_color, family='monospace')

ax1.set_ylabel("Salida Digital (Mean Code)", fontsize=11, color=text_color)
ax1.grid(True, linestyle='--', color=grid_color, alpha=0.4)
ax1.legend(loc='lower right', frameon=True, facecolor=bg_color, edgecolor=grid_color, labelcolor=text_color)

# === GRÁFICA 2: RESIDUOS (Estilo Stem/Lollipop) ===
ax2.set_facecolor(bg_color)
ax2.axhline(0, color='gray', linestyle='-', linewidth=1, alpha=0.5)

# Puntos rosas
ax2.scatter(X, residuals, color=c_resid, s=25, edgecolor='black', linewidth=0.5, zorder=5)
# Líneas verticales (Stem) conectando al cero
ax2.vlines(X, 0, residuals, color=c_resid, alpha=0.4, linewidth=1) 

ax2.set_ylabel("Error (LSB)", fontsize=10, color=text_color)
ax2.set_xlabel("Entrada Esperada (Virtual Step)", fontsize=11, color=text_color)

# Ajuste dinámico de escala Y
limit_y = max(np.max(np.abs(residuals)) * 1.3, 1.0)
ax2.set_ylim(-limit_y, limit_y)
ax2.grid(True, linestyle=':', color=grid_color, alpha=0.5)

plt.tight_layout()
plt.show()
