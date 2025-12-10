import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# --- 1. CONFIGURACIÓN DE PARÁMETROS (VALORES COMERCIALES) ---
# Constantes Físicas
C_TISSUE = 1540.0  # m/s
F_TARGET = 2.5e6   # 2.5 MHz

# Filtro Pasa Altas (Pasivo RC)
R_hp = 820      # Ohms (Comercial)
C_hp = 1e-9     # 1 nF
fc_hp_theo = 1 / (2 * np.pi * R_hp * C_hp)

# Filtro Pasa Bajas (Activo 2do Orden Sallen-Key)
R_lp = 470      # Ohms (Comercial)
C_lp = 100e-12  # 100 pF
fc_lp_theo = 1 / (2 * np.pi * R_lp * C_lp) # Simplificado R1=R2, C1=C2

# --- 2. GENERACIÓN DE DATOS (SIMULACIÓN) ---
# Rango de Frecuencias: 10 kHz a 100 MHz
f_log = np.logspace(4, 8, 1000)
w_log = 2 * np.pi * f_log

# Funciones de Transferencia
# HPF
num_hp, den_hp = [R_hp * C_hp, 0], [R_hp * C_hp, 1]
sys_hp = signal.TransferFunction(num_hp, den_hp)
_, mag_hp, _ = signal.bode(sys_hp, w_log)

# LPF (Butterworth 2do orden approx para simulación)
w0 = 2 * np.pi * fc_lp_theo
zeta = 0.707
num_lp, den_lp = [w0**2], [1, 2*zeta*w0, w0**2]
sys_lp = signal.TransferFunction(num_lp, den_lp)
_, mag_lp, _ = signal.bode(sys_lp, w_log)

# Respuesta Total
mag_total = mag_hp + mag_lp

# Obtener magnitud en la frecuencia objetivo (2.5 MHz)
idx_target = (np.abs(f_log - F_TARGET)).argmin()
gain_target = mag_total[idx_target]

# --- 3. GRAFICACIÓN (ESTILO DASHBOARD) ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(13, 7))
plt.subplots_adjust(right=0.70, top=0.85, bottom=0.15)

# Títulos
fig.suptitle(f"ANALOG FILTER STAGE | SIMULATION", fontsize=18, fontweight='bold', color='#4ade80')
ax.set_title(f"Target: {F_TARGET/1e6} MHz | Bandwidth Design | Topology: HP Passive + LP Active", fontsize=10, color='gray')

# Ejes Principales
ax.set_xlabel("Frequency (Hz)", fontsize=12, color='#bdc3c7')
ax.set_ylabel("Magnitude (dB)", fontsize=12, color='#bdc3c7')
ax.set_xlim(f_log[0], f_log[-1])
ax.set_ylim(-60, 5)
ax.grid(True, which='both', linestyle='--', alpha=0.2)
ax.set_xscale('log')

# Eje Superior (Conversión a Longitud de Onda)
ax_top = ax.secondary_xaxis('top')
def freq_to_lambda(f): return (C_TISSUE / f) * 1000 # mm
def lambda_to_freq(l): return C_TISSUE / (l / 1000)
# Nota: La escala logarítmica hace difícil usar funciones directas en secondary_axis de matplotlib a veces, 
# simplificamos etiquetas manuales o dejamos log si es compatible. 
# Para robustez visual en log, etiquetaremos manualmente el eje superior:
ax_top.set_xlabel('Wavelength in Tissue (mm)', fontsize=11, color='#f39c12')
ax_top.tick_params(axis='x', colors='#f39c12', which='both')
# Truco visual para eje log inverso (frecuencia sube, lambda baja)
ticks_freq = [1e5, 1e6, 1e7]
ticks_lambda = [freq_to_lambda(f) for f in ticks_freq]
ax_top.set_xticks(ticks_freq)
ax_top.set_xticklabels([f"{l:.2f}" for l in ticks_lambda])

# Ploteo de Líneas
line_total, = ax.plot(f_log, mag_total, color='#00f2ff', linewidth=2.0, label='Total Response')
ax.plot(f_log, mag_hp, '--', color='#4ade80', alpha=0.4, linewidth=1, label='HPF Stage')
ax.plot(f_log, mag_lp, '--', color='#ff0055', alpha=0.4, linewidth=1, label='LPF Stage')

# Marcador Target
ax.plot(F_TARGET, gain_target, 'o', color='#f39c12', markersize=6, zorder=5)
ax.axvline(F_TARGET, color='#f39c12', linestyle=':', alpha=0.5)

# --- 4. INSET ZOOM (BANDA DE PASO) ---
axins = ax.inset_axes([0.10, 0.15, 0.35, 0.35]) # Posición abajo izquierda
axins.set_facecolor('#0f172a')
axins.grid(True, linestyle=':', color='gray', alpha=0.3)
axins.plot(f_log, mag_total, color='#00f2ff', linewidth=2)
axins.set_xscale('log')

# Configurar Zoom alrededor de 2.5 MHz
zoom_f_center = F_TARGET
zoom_f_width = 1.5e6 
axins.set_xlim(zoom_f_center - 1e6, zoom_f_center + 1e6)
axins.set_ylim(-3, 1) # Ver planicidad en banda de paso
axins.set_title(f"Passband Flatness (dB)", fontsize=9, color='#00f2ff')

# Conectores del Zoom
mark_inset(ax, axins, loc1=1, loc2=3, fc="none", ec="0.5", linestyle="--")

# --- 5. PANEL LATERAL (METRICS) ---
col_x = 0.73

fig.text(col_x, 0.88, "COMPONENT VALUES", fontsize=12, fontweight='bold', color='white')
fig.text(col_x, 0.88-0.005, "__________________", fontsize=12, fontweight='bold', color='#4ade80')

props = dict(boxstyle='round', facecolor='#1e293b', alpha=0.8)
info_text = (
    f"[ HPF - Passive ]\n"
    f"R13: {R_hp} $\Omega$\n"
    f"C4:  {C_hp*1e9:.0f} nF\n\n"
    f"[ LPF - Active ]\n"
    f"R11: {R_lp} $\Omega$\n"
    f"R12: {R_lp} $\Omega$\n"
    f"C2:  {C_lp*1e12:.0f} pF\n"
    f"C3:  {C_lp*1e12:.0f} pF"
)
fig.text(col_x, 0.65, info_text, fontsize=10, family='monospace', color='#bdc3c7', bbox=props)

fig.text(col_x, 0.55, "FILTER METRICS", fontsize=12, fontweight='bold', color='white')
fig.text(col_x, 0.55-0.005, "_______________", fontsize=12, fontweight='bold', color='#4ade80')

# Métricas Calculadas
t_fc_hp = fig.text(col_x, 0.50, f"fc (HP): {fc_hp_theo/1e3:.2f} kHz", fontsize=11, family='monospace', color='white')
t_fc_lp = fig.text(col_x, 0.47, f"fc (LP): {fc_lp_theo/1e6:.2f} MHz", fontsize=11, family='monospace', color='white')
t_gain  = fig.text(col_x, 0.44, f"Gain @ Target: {gain_target:.2f} dB", fontsize=11, family='monospace', color='#f39c12')

# Estado de Validación
status_color = '#4ade80' if abs(gain_target) < 3 else '#ef4444'
status_text = "[OK] OPTIMAL" if abs(gain_target) < 3 else "[!] ATTENUATION"
t_check = fig.text(col_x, 0.38, f"Status: {status_text}", fontsize=10, fontweight='bold', color=status_color)

plt.show()
