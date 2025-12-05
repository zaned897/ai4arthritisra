"""Experiment A: Digital integrity FPGA -> PC"""

import serial
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN ---
PORT = 'COM14'
BAUD_RATE = 115200
NUM_SAMPLES = 64

# Configurar Matplotlib en modo interactivo para que la gráfica se actualice
plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], '.-', linewidth=1.0, markersize=3, label="FPGA Data")
ax.set_title("Experiment A: Digital Integrity (Live Capture)")
ax.set_xlabel("Sample (n)")
ax.set_ylabel("Digital Value (8-bit)")
ax.set_ylim(-10, 265) # Rango de 0 a 255
ax.grid(True, which='both', linestyle='--', alpha=0.7)
ax.legend()

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1) # Timeout corto para fluidez
    print(f"✅ Conectado a {PORT}. ¡Listo! Presiona el botón TRIGGER en la FPGA para iniciar el bucle continuo.")
    
    ser.reset_input_buffer()
    
    # Bucle de lectura continua
    while True:
        # Intenta leer exactamente 64 bytes.
        # Esto es NO BLOQUEANTE gracias al timeout corto.
        data = ser.read(NUM_SAMPLES)
        
        if len(data) == NUM_SAMPLES:
            values = list(data)
            
            # --- ACTUALIZAR GRÁFICA ---
            x_data = np.arange(NUM_SAMPLES)
            
            # Actualizar datos de la línea
            line.set_xdata(x_data)
            line.set_ydata(values)
            
            # Re-dibujar (Actualiza la ventana)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            # Verificar la integridad visualmente y en consola
            if values[0] == 0 and values[-1] == 63: # Chequeo rápido de rampa
                 print("⭐ Rampa recibida exitosamente.")
            else:
                 print(f"⚠️ Rampa detectada, pero secuencia puede estar incompleta. (Recibidos: {len(data)})")
                 
        # Pequeña pausa para no saturar el CPU
        plt.pause(0.001) 

except KeyboardInterrupt:
    print("\nProceso detenido por el usuario.")
except Exception as e:
    print(f"\nError: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Puerto serial cerrado.")
