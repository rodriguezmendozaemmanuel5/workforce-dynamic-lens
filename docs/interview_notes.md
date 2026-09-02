# INTERVIEW NOTES & TECHNICAL DEFENSE GUIDE (STAR METHOD)
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & HR FINANCIAL OPTIMIZATION PLATFORM

**Document Version:** v0.8.0  
**Target Audience:** Hiring Managers, People Analytics Leads, Head of BI, HR Directors, Technical Recruiters  
**Author:** Emmanuel Rodríguez Mendoza  
**Target Roles:** People Analytics Specialist / HR Data Analyst / Business Intelligence Analyst  
**Date:** August 2026  
**Status:** Certified Interview Preparation & Defense Baseline  

---

## 1. Executive Elevator Pitches

### 1.1 The 30-Second Pitch (Quick Hook)
> *"Diseñé **Workforce Dynamic Lens**, un proyecto integral de People Analytics y Business Intelligence que conecta los datos de Recursos Humanos con el estado de resultados (P&L). La solución integra un almacén analítico en **PostgreSQL**, modelado dimensional en estrella (*Star Schema*) y una suite ejecutiva en **Power BI con DAX**, identificando **$6.44M USD en riesgo financiero mitigable** por rotación en perfiles clave y ausentismo crónico, justificando un plan de retención con un **ROI proyectado del 535%**."*

### 1.2 The 2-Minute Executive Pitch (Strategic Overview)
> *"En organizaciones de tecnología y salud, la rotación voluntaria de talento técnico y el ausentismo no programado no son simples métricas operativas de RR. HH.: impactan directamente el margen EBITDA y la velocidad de los proyectos. En **MedTech Global Solutions** (4,500 colaboradores en 5 países), la dirección enfrentaba una caída del 12% en velocidad de I+D por vacantes no cubiertas y $1.3M USD en riesgo por penalizaciones de SLA en soporte hospitalario.
> 
> Para abordar este desafío desde una perspectiva cuantitativa, estructuré una solución de People Analytics de extremo a extremo:
> 1. **Entendimiento de Negocio & BRS:** Definí los requerimientos funcionales, preguntas estratégicas de talento y reglas de dominio de RR. HH.
> 2. **Modelado Dimensional en PostgreSQL:** Diseñé un modelo en estrella Kimball con soporte para dimensiones de variación lenta (SCD Tipo 2), garantizando la trazabilidad histórica de salarios y áreas sin duplicar el conteo de personal.
> 3. **Análisis Diagnóstico de Talento:** Crucé variables de competitividad salarial (*Compa-Ratio*), sobrecarga de horas extra y antigüedad para identificar focos rojos y aislar a los **315 colaboradores de alto desempeño en riesgo crítico de salida**.
> 4. **Business Intelligence & Storytelling:** Desarrollé 3 dashboards en Power BI con medidas DAX dinámicas y un simulador *What-If* que permite a los líderes modelar el retorno de inversión de planes de retención preventivos.
> 
> Mi objetivo con este proyecto fue demostrar mi capacidad para traducir necesidades complejas de Recursos Humanos en modelos de datos relacionales, indicadores visuales de alto impacto y recomendaciones estratégicas con retorno financiero."*

---

## 2. Structured Case Studies (STAR Methodology)

### 🌟 STAR Case 1: Retención de Talento Crítico en I+D & Costo de Vacancia
* **Situation (Situación):**
  MedTech Global Solutions sufría renuncias imprevistas de ingenieros de software senior en I+D. Los registros de salida mostraban respuestas genéricas ("Desarrollo Profesional"), pero cada puesto vacante tardaba entre 60 y 90 días en cubrirse, retrasando en un 12% los lanzamientos de software clínico.
* **Task (Tarea):**
  Identificar las verdaderas causas de renuncia en perfiles de alto desempeño (Performance $\ge$ 4.0), cuantificar el costo económico de vacancia en el P&L y proponer un plan de acción preventivo.
* **Action (Acción):**
  - Implementé la regla de reclasificación proxy (`BR-23`), auditando si los colaboradores renunciantes tenían salarios por debajo del punto medio de mercado (*Compa-Ratio* $< 0.85$).
  - Calculé la fórmula de **Costo de Vacancia Ponderado** (salario cargado $\times$ días de vacante $\times 1.50$ por factor de productividad en posiciones críticas).
  - Diseñé en Power BI la *Matriz de Desempeño vs. Riesgo de Salida*, visualizando claramente a los 315 Top Performers en riesgo.
* **Result (Resultado):**
  Demostré a la dirección que un ajuste de nivelación salarial focalizado de $180k USD evita pérdidas estimadas en más de **$1.2M USD** por reemplazo y vacancia, probando que retener al talento clave es sustancialmente más rentable que contratar de forma reactiva.

---

### 🌟 STAR Case 2: Diagnóstico de Ausentismo Crónico & Protección de SLAs en Soporte
* **Situation (Situación):**
  En el área de Operaciones Clínicas (soporte 24/7 a hospitales), se detectó un incremento de ausencias cortas imprevistas (1–2 días), detonando 40 incumplimientos en Acuerdos de Nivel de Servicio (SLAs) con penalizaciones por **$1.3M USD**.
* **Task (Tarea):**
  Diferenciar las incapacidades médicas justificadas del micro-ausentismo recurrente por fatiga, probar la relación con la sobrecarga de trabajo y habilitar alertas operativas.
* **Action (Acción):**
  - Implementé el **Factor de Bradford** ($B = S^2 \times D$) en SQL (`sql/analytics/13_views.sql`) y medidas DAX en ventanas móviles de 12 meses, ponderando la frecuencia de ausencias sobre el total de días planos.
  - Crucé los registros de asistencia con las horas extra acumuladas, demostrando que sobrepasar las **30 horas extra mensuales** disparaba el Bradford Score a más de 200 puntos (zona de alerta severa).
  - Construí el dashboard *Absenteeism Diagnostic & SLA Impact* en Power BI para el monitoreo de capacidad operativa por turno.
* **Result (Resultado):**
  Se estableció una política operativa con tope de 20h extra/mes y redistribución de turnos ante alertas de Bradford $> 150\text{ pts}$, proyectando una reducción del 35% en ausencias intermitentes y la eliminación de penalizaciones contractuales por falta de cobertura.

---

### 🌟 STAR Case 3: Modelado Dimensional Kimball & Trazabilidad Histórica en SQL / DAX
* **Situation (Situación):**
  Los datos de personal provenían de sistemas fragmentados y tablas planas, generando inconsistencias al calcular la evolución salarial histórica y duplicando el conteo de empleados activos.
* **Task (Tarea):**
  Diseñar un modelo dimensional en estrella (*Star Schema*) en **PostgreSQL 16+** que mantenga el histórico salarial y de promociones (SCD Tipo 2) sin distorsionar los cálculos de headcount en Power BI.
* **Action (Acción):**
  - Estructuré `dim_employees` con campos de control temporal (`valid_from`, `valid_to`, `is_current_row`, `is_active`).
  - Creé vistas analíticas en SQL con filtros `is_current_row = TRUE` y relaciones de `1:N` unidireccionales hacia las tablas de hechos (`fact_attendance_logs`, `fact_terminations`, `fact_sla_events`).
  - Desarrollé medidas DAX dinámicas en Power BI (`DISTINCTCOUNT` condicionado a la fila vigente) para asegurar exactitud tanto en la foto actual como en el análisis temporal histórico.
* **Result (Resultado):**
  Se gestionaron 1.51M de registros con **0 huérfanos y 0 duplicaciones**, superando una suite de 7 pruebas de validación en SQL y permitiendo reportes en Power BI fluidos y confiables.

---

### 🌟 STAR Case 4: Storytelling con Datos, Simulador What-If & Caso de Negocio (ROI)
* **Situation (Situación):**
  La dirección de Recursos Humanos presentaba tradicionalmente reportes de satisfacción cualitativos que no lograban justificar presupuestos ante el CFO y la Dirección General.
* **Task (Tarea):**
  Monetizar las ineficiencias de capital humano y construir una herramienta interactiva que permita simular escenarios de inversión y retorno financiero.
* **Action (Acción):**
  - Redacté el reporte ejecutivo [`docs/Business_Insights.md`](file:///e:/PROYECTOS%20PORTAFOLIO/Workforce%20Dynamic%20Lens/docs/Business_Insights.md) cuantificando los **$6.44M USD** de exposición total (vacancia, separaciones, multas SLA y reclutamiento).
  - Diseñé un simulador *What-If* en Power BI utilizando parámetros DAX desconectados para modelar reducciones porcentuales de rotación y calcular el ROI dinámico.
  - Formulé el caso de negocio: inversión inicial de $85,000 USD frente a $540,000 USD de ahorro bruto anual.
* **Result (Resultado):**
  Demostré un beneficio neto de **$455,000 USD en el Año 1**, un **ROI del 535%** y un periodo de amortización de **2.8 meses**, posicionando a People Analytics como un habilitador estratégico del P&L.

---

## 3. Technical Defense Questions (Preguntas Técnicas de Entrevista)

### P1: ¿Por qué elegiste un Esquema en Estrella (Kimball) en lugar de una tabla plana en Power BI?
> *"Un modelo dimensional en estrella separa con claridad las dimensiones descriptivas (empleados, departamentos, puestos, fechas) de las tablas de hechos transaccionales (asistencia, bajas, eventos SLA). Esto optimiza el motor VertiPaq de Power BI mediante compresión columnar, simplifica las medidas DAX evitando relaciones bidireccionales ambiguas y permite que los usuarios de negocio filtren y agreguen métricas fácilmente por cualquier jerarquía organizativa."*

---

### P2: ¿Cómo gestionaste SCD Tipo 2 en `dim_employees` para no duplicar el Headcount en DAX?
> *"En `dim_employees`, cada cambio de banda salarial o departamento genera un nuevo registro con una clave subrogada (`employee_sk`), manteniendo el mismo `employee_id` y actualizando `valid_from`, `valid_to` e `is_current_row`.
> Para que el dashboard muestre con precisión los 3,300 empleados activos actuales sin contar filas históricas duplicadas, apliqué en DAX:*
> ```dax
> Active Headcount = 
> CALCULATE(
>     DISTINCTCOUNT(dim_employees[employee_id]),
>     dim_employees[is_current_row] = TRUE,
>     dim_employees[is_active] = TRUE
> )
> ```
> *De esta forma, cuando se analiza el headcount vigente se toma únicamente la fila actual, pero cuando se analiza la evolución salarial histórica se aprovecha la trazabilidad completa del SCD2."*

---

### P3: ¿Por qué el Factor de Bradford ($S^2 \times D$) es mejor que simplemente sumar los días de ausencia?
> *"Porque en la gestión operativa de turnos, la predictibilidad del ausentismo es mucho más crítica que el volumen total de días. La fórmula $B = S^2 \times D$ eleva al cuadrado el número de instancias independientes ($S$) y lo multiplica por los días totales ($D$).
> Por ejemplo:
> - Empleado A: 1 ausencia continua de 10 días por incapacidad médica $\rightarrow 1^2 \times 10 = \mathbf{10\text{ puntos}}$ (Bajo impacto operativo, el turno se planifica y se cubre fácilmente).
> - Empleado B: 10 ausencias no programadas de 1 día $\rightarrow 10^2 \times 10 = \mathbf{1,000\text{ puntos}}$ (Riesgo crítico, desestabiliza la operación 10 veces de forma imprevista).
> El Factor de Bradford nos permitió identificar el ausentismo intermitente por agotamiento laboral y tomar acciones preventivas."*

---

### P4: ¿Cómo calculaste el impacto financiero en P&L ($6.44M USD de exposición)?
> *"Estructuré el modelo financiero sobre cuatro pilares objetivos:
> 1. **Costo de Vacancia Ponderado (`BR-16`):** $\text{Días de Vacante} \times \left(\frac{\text{Salario Cargado}}{365}\right) \times 1.50$ (factor multiplicador por pérdida de productividad en puestos críticos de I+D).
> 2. **Costos Directos de Separación:** Liquidaciones legales calculadas en `fact_terminations`.
> 3. **Penalizaciones Contractuales por SLA:** Multas registradas en `fact_sla_events` atribuidas a falta de personal en soporte hospitalario.
> 4. **Costos de Reclutamiento Externo:** Tarifas pagadas a agencias de selección (15-20% del salario base anual para posiciones técnicas).
> La suma consolidada evidenció los $6.44M USD en riesgo mitigable, sirviendo como fundamento cuantitativo del caso de negocio."*

---

### P5: ¿Qué es la Reclasificación Proxy de Motivos de Salida (`BR-23`) y por qué la implementaste?
> *"En las entrevistas de salida de RR. HH., los colaboradores suelen marcar motivos socialmente aceptables o genéricos como 'Desarrollo Profesional'. Para corregir este sesgo, implementé una regla analítica que audita las condiciones del colaborador al renunciar:
> - Si marcó 'Desarrollo Profesional' pero su `Compa-Ratio < 0.85` $\rightarrow$ Se analiza como **Inconformidad Salarial (Proxy)**.
> - Si marcó 'Desarrollo Profesional' pero acumulaba `Horas Extra > 30h/mes` $\rightarrow$ Se analiza como **Sobrecarga / Burnout (Proxy)**.
> Esto permitió a los HRBPs descubrir las verdaderas causas cuantitativas de rotación en lugar de guiarse por respuestas sesgadas."*

---

### P6: ¿Cómo aseguraste la privacidad de datos (RGPD / PII) en este proyecto?
> *"Desde la etapa de diseño (`docs/data_dictionary.md`), clasifiqué cada variable según su nivel de confidencialidad. Para proteger la privacidad, utilicé un generador en Python (`python/data_generation/`) que construyó un dataset sintético con 4,500 colaboradores y 1.51M de registros que respeta correlaciones reales de Recursos Humanos sin contener datos personales reales de ningún empleado."*

---

## 4. Matriz Rápida de Respuestas para Entrevistas (Cheat Sheet)

| Pregunta Típica | Concepto Clave / Respuesta Rápida |
| :--- | :--- |
| **¿Cuál es tu perfil profesional?** | Especialista en People Analytics y Data Analytics, enfocado en conectar datos de talento con impacto financiero en P&L mediante SQL, Power BI y DAX. |
| **¿Cuál fue tu mayor reto en el proyecto?** | Reconciliar la consistencia temporal de datos (SCD Tipo 2 y registros de asistencia) y traducir indicadores cualitativos de RR. HH. a valor económico. |
| **¿Cuál es el insight más relevante?** | Que la fuga en I+D se debía a una desalineación salarial de mercado (*Compa-Ratio < 0.85*) y que retener al personal cuesta una fracción del costo de vacancia ($1.2M USD). |
| **¿Por qué PostgreSQL + Power BI?** | PostgreSQL actúa como Data Warehouse relacional estructurado y Power BI como la suite semántica para medidas DAX avanzadas y dashboards ejecutivos. |
| **¿Cómo apoya esta herramienta a los HRBPs?** | Mediante el *Retention Action Center*, proporcionando alertas tempranas de colaboradores en riesgo para realizar Stay Interviews y ajustes de compensación. |