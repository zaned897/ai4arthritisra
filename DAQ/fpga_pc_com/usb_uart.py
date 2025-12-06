"""
Experiment A: Integridad Digital FPGA -> PC
Valida el patrón de diente de sierra (0 a 63) tolerando lecturas asíncronas.
"""

import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from matplotlib.animation import FuncAnimation

SERIAL_PORT = 'COM14'
BAUD_RATE = 115200
SAMPLE_SIZE = 1024
FS_MHZ = 27.0
BIT_DEPTH = 8

period_us = 1.0 / FS_MHZ 
time_axis = np.linspace(0, SAMPLE_SIZE * period_us, SAMPLE_SIZE)
full_scale = 2**BIT_DEPTH - 1

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    ser.reset_input_buffer()
    print(f"✅ CONECTADO: {SERIAL_PORT}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit()

# --- 3. DISEÑO VISUAL ---
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(right=0.75) # Dejar espacio a la derecha para métricas

# Títulos
ax.set_title(f"FPGA Burst Acquisition | {FS_MHZ} MSPS | Integrity Check", fontsize=14, fontweight='bold', color='#444')
ax.set_xlabel("Time of Flight ($\mu s$)", fontsize=12)
ax.set_ylabel("Digital Amplitude (LSB)", fontsize=12)
ax.set_ylim(-5, 80) # Un poco más de 63 para margen visual
ax.set_xlim(0, max(time_axis))

# Línea Principal
line_main, = ax.plot([], [], color='#2874A6', linewidth=1.2, label='Full Burst Window')

# --- 4. ZOOM MEJORADO (CON FONDO Y RAMPA COMPLETA) ---
# Ubicación: Arriba a la derecha, dentro de la gráfica
axins = ax.inset_axes([0.60, 0.55, 0.35, 0.35]) 

# FONDO DEL ZOOM (Para diferenciarlo)
axins.set_facecolor('#FFF9E3') # Color "Crema/Cornsilk" suave
axins.grid(True, linestyle=':', color='gray', alpha=0.5)

# Línea del Zoom
line_zoom, = axins.plot([], [], color='#C0392B', linewidth=1.5, marker='o', markersize=4, label='Detail View')

# CALCULO DE VENTANA DE ZOOM:
# Queremos ver 1 ciclo completo de la rampa (64 muestras)
# Tiempo = 64 * periodo
ramp_period_us = 64 * period_us # aprox 2.37 us
x_center = 5.0 # Centrado arbitrario en 5us
axins.set_xlim(x_center, x_center + ramp_period_us)
axins.set_ylim(0, 70) 
axins.set_title("Single Period Detail (Zoom)", fontsize=10, fontweight='bold')

# Conectores visuales
mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.5", linestyle="--")

# --- 5. PANEL DE MÉTRICAS LATERAL (KPIs) ---
# Usamos coordenadas de la figura (0,0 a 1,1) para poner texto fuera de la gráfica
fig.text(0.78, 0.85, "SYSTEM METRICS", fontsize=12, fontweight='bold', color='#333')

# Textos dinámicos
text_fps = fig.text(0.78, 0.80, "FPS: --", fontsize=11, family='monospace')
text_rate = fig.text(0.78, 0.77, "Data: -- kB/s", fontsize=11, family='monospace')
text_packet = fig.text(0.78, 0.74, "Pkts: 0", fontsize=11, family='monospace')
text_integrity = fig.text(0.78, 0.71, "Integrity: CHECKING", fontsize=10, fontweight='bold', color='gray')

# Variables de estado para cálculos
last_time = time.time()
packet_count = 0

def update(frame):
    global last_time, packet_count
    
    if ser.in_waiting >= SAMPLE_SIZE:
        try:
            # 1. Leer Datos
            raw = ser.read(SAMPLE_SIZE)
            data = np.array(list(raw))
            
            # 2. Actualizar Gráficas
            line_main.set_data(time_axis, data)
            line_zoom.set_data(time_axis, data)
            
            # 3. Cálculos de Rendimiento (LO QUE IMPORTA AL JURADO)
            current_time = time.time()
            dt = current_time - last_time
            if dt > 0:
                fps = 1.0 / dt
                # kB/s = (Bytes por paquete * FPS) / 1000
                data_rate = (SAMPLE_SIZE * fps) / 1000.0 
            else:
                fps = 0
                data_rate = 0
            
            last_time = current_time
            packet_count += 1
            
            # 4. Verificación de Integridad (Solo para señal de prueba)
            # Si es rampa, la diferencia entre muestras vecinas debe ser 1 (o -63 al resetear)
            diffs = np.diff(data)
            # Contamos cuántos saltos no son +1 ni el reset grande
            errors = np.sum((diffs != 1) & (diffs != -full_scale))
            
            # 5. Actualizar Textos
            text_fps.set_text(f"Refresh: {fps:4.1f} Hz")
            text_rate.set_text(f"Rate:    {data_rate:4.1f} kB/s")
            text_packet.set_text(f"Count:   {packet_count}")
            
            if errors <= 5: # Tolerancia pequeña por glitches de inicio
                text_integrity.set_text("[OK] SEQUENCE VALID")
                text_integrity.set_color('#27AE60') # Verde
            else:
                text_integrity.set_text(f"[!] DATA LOSS") 
                text_integrity.set_color('#C0392B') # Rojo

            ser.reset_input_buffer()
            
        except Exception as e:
            print(e)
            
    return line_main, line_zoom

ani = FuncAnimation(fig, update, interval=1, blit=False, cache_frame_data=False)
plt.show()
ser.close()
