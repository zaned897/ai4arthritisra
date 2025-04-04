# Protocolo de Investigación para Doctorado

## Título Propuesto
"Reconstrucción y Análisis de Imágenes de Artritis Reumatoide mediante Deep Learning"

## Introducción
La artritis reumatoide (AR) es una enfermedad crónica caracterizada por la inflamación de las articulaciones, lo que lleva a daños óseos y deformidades. La identificación temprana y precisa de AR es crucial para el tratamiento y manejo de la enfermedad. Este estudio propone el uso de técnicas de deep learning y procesamiento de imágenes para mejorar la detección y clasificación de AR.

## Objetivos
1. Desarrollar modelos de deep learning para la segmentación, detección de puntos clave y conteo de características en imágenes de AR.
2. Implementar técnicas de reconstrucción de imágenes para mejorar la visualización y análisis de articulaciones afectadas por AR.
3. Evaluar la efectividad de estos modelos en datos de imágenes médicas de alta resolución.

## Estado Actual del Proyecto

Actualmente se encuentra en desarrollo un **sistema local (demo - prototipo)** de bajo nivel para la creación de imágenes fotoacústicas. Este sistema se compone de tres módulos principales:

1. **Generación de fuente (driver de corriente):** Encargado de emitir pulsos de alta corriente y corta duración sobre un diodo láser.
2. **Adquisición de señales:** Basado en sensores ultrasónicos para captar las ondas generadas por el efecto fotoacústico.
3. **Procesamiento y reconstrucción de datos:** Aún en fases posteriores del desarrollo.

---

## Desarrollo Actual: Driver de Corriente para Diodo Láser

El presente avance se enfoca en el diseño y prueba de un **driver láser simple** basado en el siguiente circuito:

![Driver Circuito](docs/doc_images/simple_driver_diagram.png)

Este circuito permite la generación de pulsos de corriente de alta intensidad (hasta 60 A), con anchos de pulso inferiores a 10 ns, y tasas de repetición mayores a 500 kHz.

### Descripción del Funcionamiento

- El capacitor **C** se carga a un alto voltaje **HV** a través del resistor **R_C** y el diodo **D1**.
- Una señal externa **TTL** activa el transistor MOSFET **Q1**, descargando **C** directamente sobre el diodo láser **LD**.
- **R_CL** limita la corriente máxima sobre el láser.
- **R_M** permite monitorear la corriente mediante caída de voltaje.
- La duración del pulso se ajusta modificando el valor de **C**.
- El diseño está inspirado en sistemas para aplicaciones de radar láser, optimizado para pulsos ultra rápidos y corrientes elevadas.

### Componentes Usados (Valores Típicos)

| Componente | Descripción                             | Valor Típico       |
|------------|-----------------------------------------|--------------------|
| **Q1**     | MOSFET de potencia (DE275-501N16A)      | 500 V / 50 A       |
| **C**      | Capacitor de descarga                   | ~400 pF            |
| **R_C**    | Resistor de carga del capacitor         | ~3.4 kΩ            |
| **R_CL**   | Resistor limitador de corriente         | ~1 Ω               |
| **R_M**    | Resistor de monitoreo                   | ~0.1 Ω             |
| **D1**     | Diodo rápido para proteger el circuito  | Tipo Schottky      |
| **LD**     | Diodo láser                             | Según aplicación   |

---

## Simulación del Driver

A continuación se muestra una simulación básica del funcionamiento del circuito:

![Simulación del Driver](docs/doc_images/simple_simultion.gif)

Esta simulación confirma la descarga rápida del capacitor sobre la carga (LD) y el control de la forma del pulso mediante el valor del capacitor y el MOSFET.

---

Este driver constituye el primer paso hacia la generación controlada de señales fotoacústicas, necesarias para la fase de adquisición y reconstrucción de imágenes médicas.


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
