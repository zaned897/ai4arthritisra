# Especificaciones de Filtros y Sistema de Adquisición

Basado en el análisis del documento `amplifier_content.pdf` (páginas 106-111 de las Memorias del Congreso Celaya 2016), se detallan las especificaciones de la etapa de filtrado analógico y parámetros relevantes del sistema.

## Etapa de Filtrado Analógico
El sistema utiliza una configuración en cascada de dos filtros para acondicionar la señal ECG.

### 1. Filtro Pasa Altas (High Pass)
Elimina componentes de baja frecuencia (DC offset).
*   **Tipo:** Pasivo de primer orden (RC).
*   **Frecuencia de Corte ($f_{cPa}$):** $0.482 \text{ Hz}$.
*   **Atenuación:** -3dB en $f_{cPa}$.
*   **Componentes:**
    *   $R_{13} = 3.3 \text{ M}\Omega$
    *   $C_4 = 100 \text{ nF}$
*   **Ecuación:** $f_{cPa} = \frac{1}{2\pi R_{13}C_4}$

### 2. Filtro Pasa Bajas (Low Pass)
Limita el ancho de banda para evitar aliasing y ruido de alta frecuencia.
*   **Tipo:** Activo de segundo orden (Sallen-Key).
*   **Frecuencia de Corte ($f_{cPb}$):** $102.78 \text{ Hz}$.
*   **Atenuación:** -40dB en $f_{cPb}$ (según documento).
*   **Componentes:**
    *   $R_{11} = 5.1 \text{ k}\Omega$
    *   $R_{12} = 10 \text{ k}\Omega$
    *   $C_3 = 100 \text{ nF}$
    *   $C_2 = 470 \text{ nF}$
*   **Ecuación:** $f_{cPb} = \frac{1}{2\pi \sqrt{R_{11}R_{12}C_3C_2}}$

## Contexto del Sistema
Parámetros adicionales del sistema de adquisición que influyen en el diseño de los filtros:

*   **Ganancia del Amplificador de Instrumentación:** $\Delta \approx 603.44$ (calculada con $R_1 = 82\Omega$).
*   **Frecuencia de Muestreo ($f_s$):** $200 \text{ Hz}$ (Periodo $t_s = 5 \text{ ms}$).
*   **Resolución A/D:** 10 bits (0-5V), $\approx 4.9 \text{ mV/bit}$.
*   **Alimentación:** Batería de 3.7V (elimina ruido de 60Hz de línea).

## Referencias
Datos extraídos de las secciones "Filtrado analógico", "Amplificador de instrumentación" y "Adquisición de datos".
