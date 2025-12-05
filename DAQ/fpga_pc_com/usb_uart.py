"""
Experiment A: Integridad Digital FPGA -> PC
Valida el patrón de diente de sierra (0 a 63) tolerando lecturas asíncronas.
"""

import serial
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN ---
PORT = 'COM14'
BAUD_RATE = 115200
NUM_SAMPLES = 64
RAMP_MAX_VALUE = NUM_SAMPLES - 1 # 63

def validar_rampa_ciclica(valores):
    """
    Verifica si la secuencia recibida es una rotación perfecta de la rampa ideal (0 a 63).
    Esto resuelve el problema de la lectura asíncrona (wrap-around).
    """
    if len(valores) != NUM_SAMPLES:
        return False, "Tamaño incorrecto"

    # 1. Generar la secuencia ideal (0, 1, ..., 63)
    ideal_ramp = list(range(NUM_SAMPLES))
    
    # 2. Crear una secuencia duplicada para chequear la rotación (0, 1, ..., 63, 0, 1, ...)
    ideal_double = ideal_ramp + ideal_ramp
    
    # 3. Verificar la integridad de la rampa.
    # Buscamos la primera ocurrencia del primer valor recibido (valores[0]) en la rampa ideal.
    try:
        start_index = ideal_double.index(valores[0])
    except ValueError:
        # Si el primer valor no está en la rampa ideal (ej. es basura), falla.
        return False, "Valor fuera de rango"

    # 4. Generar la secuencia esperada a partir de ese índice.
    expected_sequence = ideal_double[start_index : start_index + NUM_SAMPLES]

    # 5. Comparar byte a byte.
    is_perfect = (expected_sequence == valores)
    
    return is_perfect, f"Secuencia OK. Iniciada en {valores[0]}."


# --- PLOT Y BUCLE DE LECTURA ---

plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], '.-', linewidth=1.0, markersize=3, label="FPGA Data")
ax.set_title("Experimento A: Integridad Digital (Live Capture)")
ax.set_xlabel(f"Muestra (0 a {RAMP_MAX_VALUE})")
ax.set_ylabel("Valor Digital (0 a 255)")
ax.set_ylim(-10, 265) 
ax.set_xlim(-10,70)
ax.grid(True, which='both', linestyle='--', alpha=0.7)
ax.legend()
text_status = ax.text(0.5, 0.95, '', transform=ax.transAxes, ha='center', fontsize=12, color='black')


try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.05) 
    print(f"✅ Conectado a {PORT}. ¡Cargando bucle!")
    ser.reset_input_buffer()
    
    # Bucle de lectura continua
    while True:
        data = ser.read(NUM_SAMPLES)
        
        if len(data) == NUM_SAMPLES:
            values = list(data)
            
            # --- VALIDACIÓN ROBUSTA ---
            is_perfect, status_msg = validar_rampa_ciclica(values)
            
            # --- ACTUALIZAR CONSOLA Y GRÁFICA ---
            
            # 1. Gráfica
            line.set_xdata(np.arange(NUM_SAMPLES))
            line.set_ydata(values)
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            # 2. Consola y Status
            if is_perfect:
                print(f"⭐ ÉXITO: {status_msg}")
                text_status.set_text(f"ÉXITO: BER 0% | {status_msg}")
                text_status.set_color('green')
            else:
                print(f"❌ FALLO: Secuencia rota o no cíclica. {status_msg}")
                text_status.set_text(f"FALLO: Secuencia rota. {status_msg}")
                text_status.set_color('red')

        plt.pause(0.001) 

except KeyboardInterrupt:
    print("\nProceso detenido por el usuario.")
except Exception as e:
    print(f"\nError de Serial/Conexión: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Puerto serial cerrado.")