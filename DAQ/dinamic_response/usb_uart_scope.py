import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.fft import fft, fftfreq # pip install scipy

# --- CONFIGURACIÓN ---
SERIAL_PORT = 'COM14'
BAUD_RATE = 115200
SAMPLE_SIZE = 1024
FS_MHZ = 27.0 

# --- CONEXIÓN ---
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    ser.reset_input_buffer()
    print(f"System Ready: Dynamic Response Mode")
except Exception as e:
    print(f"Error: {e}")
    exit()

# --- INTERFAZ GRÁFICA ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(12, 8))
fig.suptitle(f"EXPERIMENT C: DYNAMIC RESPONSE", fontsize=16, fontweight='bold', color='#4ade80')

# Layout: Arriba (Tiempo), Abajo (Frecuencia)
gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.3)
ax_time = fig.add_subplot(gs[0])
ax_freq = fig.add_subplot(gs[1])

# --- GRÁFICA TIEMPO (OSCILOSCOPIO) ---
time_axis = np.arange(SAMPLE_SIZE) * (1/FS_MHZ) # microsegundos
line_time, = ax_time.plot([], [], color='#00f2ff', linewidth=1.5, label='RF Signal')

ax_time.set_title("Time Domain Reconstruction", fontsize=10, color='gray')
ax_time.set_ylabel("Amplitude (ADC Code)", fontsize=11, color='#bdc3c7')
ax_time.set_xlabel("Time ($\mu s$)", fontsize=11, color='#bdc3c7')
ax_time.set_ylim(-10, 265)
ax_time.set_xlim(0, 10) # Zoom a los primeros 10us para ver la onda
ax_time.grid(True, linestyle='--', alpha=0.2)

# Zoom Inserto (Detalle de la onda)
axins = ax_time.inset_axes([0.65, 0.60, 0.30, 0.35])
line_zoom, = axins.plot([], [], color='#fbbf24', marker='o', markersize=2)
axins.set_facecolor('#0f172a')
axins.set_xlim(2, 4) # Ventana de 2us
axins.set_ylim(0, 255)
axins.set_xticks([])
axins.set_yticks([])
ax_time.indicate_inset_zoom(axins, edgecolor="gray")

# --- GRÁFICA FRECUENCIA (FFT) ---
line_fft, = ax_freq.plot([], [], color='#f472b6', linewidth=1.5)
ax_freq.set_title("Frequency Domain (FFT)", fontsize=10, color='gray')
ax_freq.set_ylabel("Magnitude (dB)", fontsize=11, color='#bdc3c7')
ax_freq.set_xlabel("Frequency (MHz)", fontsize=11, color='#bdc3c7')
ax_freq.set_xlim(0, 2.0) # Ver hasta 2 MHz
ax_freq.set_ylim(0, 100)
ax_freq.grid(True, linestyle=':', alpha=0.3)

# Textos de Métricas
t_freq = fig.text(0.75, 0.05, "Dom. Freq: -- kHz", fontsize=12, fontweight='bold', color='#f472b6')
t_vpp = fig.text(0.55, 0.05, "Vpp: -- LSB", fontsize=12, fontweight='bold', color='#00f2ff')
t_bw = fig.text(0.15, 0.05, "System Bandwidth: OK", fontsize=12, color='#4ade80')

def update(frame):
    if ser.in_waiting >= SAMPLE_SIZE:
        try:
            raw = ser.read(SAMPLE_SIZE)
            data = np.array(list(raw))
            
            # 1. Update Time Plot
            line_time.set_data(time_axis, data)
            line_zoom.set_data(time_axis, data)
            
            # 2. Calculate FFT
            N = SAMPLE_SIZE
            yf = fft(data)
            xf = fftfreq(N, 1/FS_MHZ) # Eje de frecuencia en MHz
            
            # Tomamos solo la mitad positiva del espectro
            idx_pos = np.where((xf > 0.05) & (xf < 13.5))
            x_plot = xf[idx_pos]
            y_plot = np.abs(yf[idx_pos])
            
            # Normalización a dB (simple)
            y_plot_db = 20 * np.log10(y_plot + 1e-6)
            y_plot_db = y_plot_db - np.max(y_plot_db) + 80 # Offset visual
            
            line_fft.set_data(x_plot, y_plot_db)

            # 3. Métricas
            # Encontrar pico de frecuencia
            peak_idx = np.argmax(y_plot)
            dom_freq = x_plot[peak_idx] * 1000 # a kHz
            
            vpp = np.max(data) - np.min(data)

            t_freq.set_text(f"Dom. Freq: {dom_freq:.1f} kHz")
            t_vpp.set_text(f"Vpp: {vpp} LSB")
            
            # Indicador de validación
            if 400 < dom_freq < 440:
                t_bw.set_text("STATUS: [SIGNAL LOCK]")
                t_bw.set_color('#4ade80')
            else:
                t_bw.set_text("STATUS: [SEARCHING]")
                t_bw.set_color('gray')

            ser.reset_input_buffer()
        except Exception as e:
            pass
    return line_time, line_fft

ani = FuncAnimation(fig, update, interval=10, blit=False, cache_frame_data=False)
plt.show()
ser.close()
