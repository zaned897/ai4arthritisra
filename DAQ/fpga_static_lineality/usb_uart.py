import serial
import time
import numpy as np
import pandas as pd # Necesitarás instalar pandas: pip install pandas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- CONFIGURACIÓN ---
SERIAL_PORT = 'COM14' 
BAUD_RATE = 115200
SAMPLE_SIZE = 1024

# --- INICIALIZACIÓN ---
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    ser.reset_input_buffer()
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Almacenamiento de datos
data_log = []
last_logged_val = -1 # Para evitar guardar repetidos

# Configuración Gráfica
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], color='#00f2ff', label='Live Signal')

ax.set_title("Auto-Logging Linearity Test", fontsize=14, color='#4ade80')
ax.set_ylim(-10, 270)
ax.set_xlim(0, SAMPLE_SIZE)
ax.grid(True, alpha=0.3)

# Textos en pantalla
status_text = ax.text(0.02, 0.95, "Waiting...", transform=ax.transAxes, color='white')
count_text = ax.text(0.02, 0.90, "Steps Logged: 0", transform=ax.transAxes, color='yellow')

def update(frame):
    global last_logged_val
    
    if ser.in_waiting >= SAMPLE_SIZE:
        try:
            # 1. Leer datos
            raw = ser.read(SAMPLE_SIZE)
            data = np.array(list(raw))
            
            # 2. Calcular promedio (El valor DC actual)
            current_mean = np.mean(data)
            rounded_val = int(round(current_mean))
            std_dev = np.std(data)

            # 3. Actualizar gráfica
            line.set_data(range(SAMPLE_SIZE), data)
            
            # 4. LÓGICA DE GUARDADO (LOGGING)
            # Solo guardamos si el valor es nuevo (escalón subió) y es estable
            if rounded_val > last_logged_val and std_dev < 1.0:
                timestamp = time.strftime("%H:%M:%S")
                
                # Guardar en la lista en memoria
                data_log.append({
                    "Time": timestamp,
                    "Step": rounded_val,
                    "Measured_Mean": current_mean,
                    "Std_Dev": std_dev
                })
                
                # Guardar en CSV inmediatamente (append mode real simulado)
                df = pd.DataFrame(data_log)
                df.to_csv("linearity_data.csv", index=False)
                
                print(f"LOGGED -> Step: {rounded_val} | Mean: {current_mean:.4f}")
                last_logged_val = rounded_val

            # Actualizar textos
            status_text.set_text(f"Current Level: {current_mean:.2f}")
            count_text.set_text(f"Steps Logged: {len(data_log)}")
            
            # Auto-Reset visual si el FPGA da la vuelta a 0
            if rounded_val < last_logged_val and rounded_val == 0:
                 last_logged_val = -1
                 print("--- CYCLE RESET ---")

            ser.reset_input_buffer()
        except Exception as e:
            pass

    return line, status_text, count_text

ani = FuncAnimation(fig, update, interval=10, blit=False)
plt.show()
ser.close()
