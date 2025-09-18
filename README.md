# Protocolo de Investigación para Doctorado

## Título Propuesto

**"Reconstrucción y Análisis de Imágenes de Artritis Reumatoide mediante Deep Learning"**

---

## Introducción

La artritis reumatoide (AR) es una enfermedad crónica caracterizada por la inflamación de las articulaciones, lo que lleva a daños óseos y deformidades. La identificación temprana y precisa de AR es crucial para el tratamiento y manejo de la enfermedad. Este estudio propone el uso de técnicas de deep learning y procesamiento de imágenes para mejorar la detección y clasificación de AR.

---
****
- Desarrollar modelos de deep learning para la segmentación, detección de puntos clave y conteo de características en imágenes de AR.  
- Implementar técnicas de reconstrucción de imágenes para mejorar la visualización y análisis de articulaciones afectadas por AR.  
- Evaluar la efectividad de estos modelos en datos de imágenes médicas de alta resolución.  

---

## Estado Actual del Proyecto

Actualmente se encuentra en desarrollo un sistema local (**demo - prototipo**) de bajo nivel para la creación de imágenes fotoacústicas. Este sistema se compone de tres módulos principales:

1. **Generación de fuente (driver de corriente):** Encargado de emitir pulsos de alta corriente y corta duración sobre un diodo láser. *(Módulo en desarrollo activo)*.  
2. **Adquisición de señales:** Basado en sensores ultrasónicos para captar las ondas generadas por el efecto fotoacústico.  
3. **Procesamiento y reconstrucción de datos:** Aún en fases posteriores del desarrollo.  

![Circuito Panelizado v4](circuits\lumat_avalanche_driver_v3\production_v4\panelization\panelization_production_v4\panelization_production_v4.png)

---

## Desarrollo del Driver de Corriente para Diodo Láser

El enfoque actual es el diseño y la fabricación de un driver de potencia para un diodo láser, capaz de generar pulsos de corriente de alta intensidad y corta duración. El diseño ha pasado por varias iteraciones para mejorar su rendimiento, fiabilidad y funcionalidad.

### Evolución del Diseño

A continuación, se describe la progresión de las versiones del driver:

- **Versión 1 (simple_current_driver_v1):**  
  Fase conceptual y de simulación utilizando el software LiveWire. Se exploraron dos topologías: un circuito RC simple y una configuración basada en un transistor en modo avalancha. Esta última fue seleccionada como base para el desarrollo del hardware por su capacidad para generar pulsos ultrarrápidos.  

- **Versión 2 (reference_avalanche_driver_v2):**  
  Primer prototipo físico del driver en modo avalancha. Se generaron los archivos de producción (Gerbers), pero durante las pruebas se detectó un punto de fallo crítico: la resistencia de potencia se sobrecalentaba y terminaba quemándose, lo que indicaba la necesidad de un rediseño para mejorar la gestión térmica y de potencia.  

- **Versión 3 (simple_modified_v3):**  
  Primera revisión mayor del diseño. Se solucionó el problema de sobrecalentamiento sustituyendo el componente anterior por una resistencia de potencia de 10W. Además, se integró un microcontrolador Raspberry Pi Pico (RP2040) para funcionar como un generador de señal de disparo (**trigger**) preciso y programable.  

- **Versión 4 (production_v4):**  
  Versión actual y primera candidata para producción. Sobre la base de la v3, se han añadido características para mejorar su usabilidad y robustez. Las mejoras incluyen:
  - Integración de un display I2C para visualizar parámetros en tiempo real.  
  - Implementación de control de frecuencia para ajustar la tasa de repetición de los pulsos.  
  - Revisión completa de las reglas de diseño (**DRC**) para asegurar la fiabilidad en la fabricación.  
  - Panelización del diseño para la producción de múltiples unidades de forma eficiente.  

---

## Estructura del Repositorio de Diseño Electrónico

El proyecto `lumat_avalanche_driver_v3` contiene toda la historia del desarrollo electrónico.

    lumat_avalanche_driver_v3/
    │
    ├── libs/                  # Librerías de KiCad (símbolos, huellas) para componentes personalizados (RP2040, Resistencia 10W, etc.).
    │
    ├── production_v4/         # Versión 4, lista para fabricación.
    │   └── avalanche_lumat/   # Archivos de proyecto de KiCad (esquemático, PCB, Gerbers).
    │
    ├── simple_modified_v3/    # Versión 3, con RP2040 y resistencia de 10W.
    │
    ├── reference_avalanche_driver_v2/ # Versión 2, prototipo inicial con fallo.
    │
    └── simple_current_driver_v1/ # Versión 1, archivos de simulación en LiveWire.

---

## Resultados Obtenidos


## Revisión de Literatura

### Contexto de la Problemática y Retos
1. **Diagnóstico Temprano y Preciso:**
   - Aletaha, D., et al. "2010 Rheumatoid Arthritis Classification Criteria: An American College of Rheumatology/European League Against Rheumatism Collaborative Initiative." *Arthritis & Rheumatology*. 
   - McInnes, I. B., et al. "The pathogenesis of rheumatoid arthritis." *N Engl J Med*.

2. **Influencia de Factores Genéticos y Ambientales:**
   - Svendsen, A. J., et al. "On the Origin of the Human Leukocyte Antigen-DRB1 Associations with Rheumatoid Arthritis." *Arthritis & Rheumatology*.

3. **Variabilidad en la Manifestación Clínica:**
   - Smolen, J. S., et al. "Rheumatoid arthritis." *Nature Reviews Disease Primers*.

4. **Nuevas Terapias y Tratamientos:**
   - Singh, J. A., et al. "2015 American College of Rheumatology Guideline for the Treatment of Rheumatoid Arthritis." *Arthritis Care & Research*.

### Trabajos en el Estado del Arte

1. **Deep Learning en la Detección de AR:**
   - Folle, L., et al. "Deep Learning-Based Classification of Inflammatory Arthritis by Identification of Joint Shape Patterns." *Frontiers in Medicine*.

2. **Clasificación de Imágenes Médicas:**
   - Litjens, G., et al. "A survey on deep learning in medical image analysis." *Medical Image Analysis*.

3. **Fusión de Datos de Múltiples Modalidades:**
   - Yang, F., et al. "Automated Detection of Rheumatoid Arthritis Using Convolutional Neural Networks." *Journal of Digital Imaging*.

4. **Modelos de Transferencia de Aprendizaje:**
   - Tajbakhsh, N., et al. "Convolutional Neural Networks for Medical Image Analysis: Full Training or Fine Tuning?" *IEEE Transactions on Medical Imaging*.

5. **Evaluación de Tratamientos mediante IA:**
   - Sun, W., et al. "Computational modeling and analysis of rheumatoid arthritis progression: a deep learning-based approach." *PLoS ONE*.

## Metodología

### Recolección de Datos
- **Interna:** Desarrollo de un sistema de reconstrucción de imágenes utilizando imágenes indirectas por SPR y reconstrucción de imágenes termo-acústicas.
- **Externa:** Uso de bases de datos públicas como el Rheumatoid Arthritis Bioinformatics Center (RABC).

### Procesamiento de Imágenes
- **Preprocesamiento:** Limpieza y normalización de imágenes.
- **Segmentación y Análisis:** Uso de CNNs para la segmentación de áreas afectadas y detección de puntos clave en articulaciones.

### Implementación de Modelos
- **Reconstrucción de Imágenes:** Implementación de técnicas de deep learning para mejorar la visualización de articulaciones dañadas.
- **Modelos de Clasificación:** Entrenamiento de modelos para la detección y clasificación de AR en diferentes etapas y subtipos.

### Evaluación y Validación
- **Validación Cruzada:** Uso de validación cruzada y métricas como la AUROC para evaluar la efectividad de los modelos.
- **Estudios Clínicos:** Comparación de resultados con métodos diagnósticos actuales y validación mediante estudios clínicos.

## Resultados Esperados
1. Modelos de deep learning precisos para la segmentación y clasificación de imágenes de AR.
2. Técnicas de reconstrucción que mejoren la visualización y análisis de articulaciones.
3. Un sistema robusto para el diagnóstico y monitoreo de AR, con potencial de aplicación clínica.

## Cronograma
1. **Primer Semestre:** Preparación del protocolo de investigación.
2. **Fase 1 (Semestres 2-3):** Recolección y preprocesamiento de datos (12 meses).
3. **Fase 2 (Semestres 4-6):** Desarrollo y entrenamiento de modelos (18 meses).
4. **Fase 3 (Semestres 7-8):** Evaluación y validación clínica (12 meses).
5. **Fase 4 (Semestres 9-10):** Publicación y difusión de resultados (12 meses).

## Sustento Matemático

### Matemáticas en Investigación de IA
- **Funciones de Coste:** Uso de funciones de pérdida como Cross-Entropy Loss y Mean Squared Error para entrenamiento de redes neuronales.
- **Cuantización para Pesos:** Implementación de técnicas de cuantización para optimizar el almacenamiento y procesamiento en modelos de deep learning.
- **Funciones de Activación:** Investigación y aplicación de funciones de activación avanzadas como ReLU, Leaky ReLU y Swish para mejorar la eficiencia de los modelos.

### Estadística
- **Análisis de Varianza (ANOVA):** Utilizado para comparar la variabilidad entre grupos y determinar la significancia estadística de los resultados.
- **Regresión Logística:** Aplicada para la predicción de probabilidades de clasificación en modelos de deep learning.
- **Validación Cruzada:** Implementación de técnicas de validación cruzada para asegurar la generalización de los modelos.

### Matemáticas en el Procesamiento de Imágenes
- **Transformada de Fourier:** Utilizada para la filtración y análisis de frecuencias en imágenes médicas.
- **Filtros Espaciales:** Implementación de filtros de convolución para la mejora y detección de características en imágenes.
- **Transformada de Wavelet:** Aplicada para la compresión y análisis multi-resolución de imágenes médicas.

## Bibliografía
1. Aletaha, D., et al. "2010 Rheumatoid Arthritis Classification Criteria." *Arthritis & Rheumatology*.
2. McInnes, I. B., et al. "The pathogenesis of rheumatoid arthritis." *N Engl J Med*.
3. Svendsen, A. J., et al. "On the Origin of the Human Leukocyte Antigen-DRB1 Associations with Rheumatoid Arthritis." *Arthritis & Rheumatology*.
4. Smolen, J. S., et al. "Rheumatoid arthritis." *Nature Reviews Disease Primers*.
5. Singh, J. A., et al. "2015 American College of Rheumatology Guideline for the Treatment of Rheumatoid Arthritis." *Arthritis Care & Research*.
6. Folle, L., et al. "Deep Learning-Based Classification of Inflammatory Arthritis by Identification of Joint Shape Patterns." *Frontiers in Medicine*.
7. Litjens, G., et al. "A survey on deep learning in medical image analysis." *Medical Image Analysis*.
8. Yang, F., et al. "Automated Detection of Rheumatoid Arthritis Using Convolutional Neural Networks." *Journal of Digital Imaging*.
9. Tajbakhsh, N., et al. "Convolutional Neural Networks for Medical Image Analysis: Full Training or Fine Tuning?" *IEEE Transactions on Medical Imaging*.
10. Sun, W., et al. "Computational modeling and analysis of rheumatoid arthritis progression: a deep learning-based approach." *PLoS ONE*.
