# BUSINESS REQUIREMENTS DOCUMENT (BRD)
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & WORKFORCE DYNAMICS SOLUTION

**Document Version:** v0.3.0 (Refined Business Scope)  
**Target Audience:** Executive Committee (CFO, CHRO, CIO, VP of Operations)  
**Author:** Emmanuel Rodríguez Mendoza  
**Professional Role:** People Analytics / HR Data Analyst  
**Project:** Workforce Dynamic Lens  
**Date:** 2026-07-29  
**Status:** Baseline Functional Specification Approved  

---

## 1. Document Purpose

El propósito de este **Business Requirements Document (BRD)** es establecer la especificación funcional y operativa oficial de la plataforma **Workforce Dynamic Lens (v0.3.0)** para MedTech Global Solutions. Este documento actúa como el contrato funcional vinculante entre las necesidades estratégicas del negocio (definidas en el *Business Case* v0.3.0) y el diseño técnico que se detallará posteriormente en `Architecture.md`.

### Scope Boundary
Este documento define exclusivamente **qué** debe lograr la plataforma para proteger el margen EBITDA y la cartera de **$3.2M USD** en contratos B2B de telemedicina. Delimita el comportamiento del negocio para 4,500 colaboradores en LATAM y Europa. **No dicta la implementación tecnológica concreta**, la infraestructura en la nube, ni los algoritmos específicos de cifrado o modelado, delegando esas decisiones a la fase de diseño de arquitectura.

---

## 2. Business Objectives

La plataforma **Workforce Dynamic Lens** permitirá a MedTech Global Solutions alcanzar los siguientes objetivos estratégicos medibles en un horizonte de 12 meses post-despliegue:

1. **Financial Optimization & Cost Recovery:** Recuperar **$540,000 USD** brutos anuales mediante la reducción de costos directos e indirectos de vacancia, la eliminación de penalizaciones contractuales por SLA y la disminución de tarifas por intermediación de agencias de reclutamiento externo.
2. **Targeted High-Performer Retention:** Incrementar la retención voluntaria en el departamento de Investigación y Desarrollo (I+D) en empleados con desempeño superior (≥ 4/5), diagnosticando factores y perfiles de riesgo de salida.
3. **SLA Protection & Capacity Continuity:** Eliminar al 100% las penalizaciones contractuales por incumplimiento de SLA en contratos B2B de telemedicina atribuibles a déficit de personal en Soporte Clínico.
4. **Absenteeism Severity Control:** Controlar la severidad del ausentismo no programado en Soporte Clínico, reduciendo el indicador de impacto operativo por ausencias cortas recurrentes.
5. **Strategic Workforce Planning:** Reducir en un **20%** el tiempo para alcanzar la máxima productividad (*Time-to-Full Productivity*) en posiciones técnicas mediante visibilidad anticipada de la capacidad operativa y brechas de dotación.

---

## 3. Business Problems

La plataforma resolverá cuatro problemas de negocio fundamentales:

1. **Fuga Friccional de Talento Clave en I+D:** Pérdida no anticipada de ingenieros de software senior que provoca una caída del **12% en la velocidad de desarrollo** de productos.
2. **Desgaste Operativo y Ausentismo en Soporte Clínico:** Patrones de micro-ausentismo recurrente causados por sobrecarga de horas extra, desestabilizando turnos de atención y poniendo en riesgo contratos de **$3.2M USD**.
3. **Causas Raíz Ocultas por Sesgo de Origen:** Opciones genéricas en los sistemas actuales que ocultan que la causa real de renuncia es la combinación de desactualización salarial y sobrecarga operativa.
4. **Desconexión entre Gestión Humana y el P&L:** Falta de modelos monetizados que impiden justificar intervenciones preventivas de retención con retorno económico directo.

---

## 4. Stakeholders

| Stakeholder | Primary Role | Influence | Interest | Core Business Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Chief Financial Officer (CFO)** | Financial Approval & P&L Owner | High | High | Project ROI (%) / Net P&L Savings |
| **Chief HR Officer (CHRO)** | Executive HR Sponsor | High | High | High-Performer Retention Rate (%) |
| **Chief Information Officer (CIO)** | Security & Governance Sponsor | High | Medium | Enterprise Compliance & Security |
| **VP of Operations & R&D** | Operational Delivery Owner | High | High | SLA Compliance (%) / Delivery Velocity |
| **People Analytics Manager** | Solution Product Owner | Medium | High | Model Actionable Utility & Data Integrity |
| **HR Business Partners (HRBPs)** | Operational Intervention Execution | Medium | High | Individual Flight Risk & Compa-Ratio |

---

## 5. User Personas

* **CHRO (Elena Rostova):** Requiere un dashboard estratégico mensual para monitorear la tasa de retención de alto desempeño y el impacto económico global de la gestión de talento.
* **CFO (Marcus Vance):** Consulta revisiones trimestrales sobre el ahorro neto en P&L, varianza de costos de horas extra y simulaciones financieras *What-If*.
* **HRBP Senior (Carlos Mendoza):** Utiliza semanalmente el centro de acción para revisar alertas individuales de riesgo de salida y justificantes de nivelación salarial.
* **HR Director (Sarah Jenkins):** Analiza bi-semanalmente la equidad interna y la distribución de bandas salariales por país y departamento.
* **People Analytics Manager (David Chen):** Supervisa continuamente el rendimiento de la ingesta de datos, deriva de variables y métricas de utilidad de los modelos.
* **VP de Operaciones (Johan Lindqvist):** Revisa diariamente la disponibilidad de capacidad operativa y alertas de ausentismo crítico por turno.

---

## 6. Business Questions

La plataforma responderá a las siguientes **preguntas estratégicas** clasificadas por área:

### Dominio 1: Rotación Voluntaria y Riesgo de Fuga
1. ¿Cuál es la tasa de rotación voluntaria acumulada en I+D segmentada por nivel de puesto y región en el año fiscal?
2. ¿En qué intervalo de antigüedad (*tenure*) se concentra el pico de renuncias del personal de alto desempeño?
3. ¿Qué colaboradores presentan un nivel de riesgo de salida prioritario en los próximos 90 días?
4. ¿Qué combinación de factores (horas extra, brecha salarial, antigüedad) explica el riesgo de salida de un empleado individual?
5. ¿Cómo difiere la rotación voluntaria entre colaboradores en modalidad remota y presencial?
6. ¿Cuál es la proporción de deserciones que ocurren durante el primer año de servicio (*First-Year Attrition*)?

### Dominio 2: Ausentismo y Capacidad Operativa
7. ¿Cuál es la distribución del Factor de Bradford por departamento y qué proporción de la plantilla supera los umbrales de alerta configurados?
8. ¿Existe una relación medible entre la acumulación de horas extra y la frecuencia de ausencias cortas no programadas?
9. ¿Cuántas horas-hombre de capacidad operativa se pierden por ausentismo no programado por centro operativo?
10. ¿Cómo se distribuye el ausentismo según el día de la semana para identificar patrones adyacentes a descansos?
11. ¿Qué proporción del ausentismo corresponde a licencias médicas prolongadas vs. ausencias intermitentes de corta duración?

### Dominio 3: Compensación y Competitividad Salarial
12. ¿Cuál es el *Compa-Ratio* promedio de la empresa segmentado por área, nivel jerárquico y género?
13. ¿Qué porcentaje de empleados de alto desempeño se ubican en la zona inferior de su banda salarial de mercado?
14. ¿Existen diferencias salariales por género al controlar por variables de confusión (experiencia, nivel, desempeño)? *(La técnica estadística específica se determinará tras el análisis exploratorio de datos).*
15. ¿Cuál es la inversión estimada requerida para nivelar al punto medio de mercado a los colaboradores clave en riesgo de salida?
16. ¿Cómo se compara la variación salarial promedio frente a los marcadores de mercado y la rotación observada?

### Dominio 4: Desempeño y Desarrollo
17. ¿Cómo se ubican los colaboradores en la matriz de Desempeño vs. Potencial al cruzar su nivel de riesgo de salida?
18. ¿Existen variaciones sistemáticas en las evaluaciones otorgadas por diferentes líderes (posible sesgo de evaluación)?
19. ¿Cuál es la tasa de retención del personal identificado en programas de alto potencial?
20. ¿Qué relación existe entre la participación en programas de desarrollo técnico y la retención en roles junior?

### Dominio 5: Impacto Financiero y Vacancia
21. ¿Cuál es el costo financiero total de la rotación acumulado en el año, dividiendo costos directos e indirectos?
22. ¿Cuál es el impacto económico acumulado por penalizaciones de SLA derivadas de déficit de personal?
23. ¿Cuál es el beneficio financiero neto proyectado al aplicar las propuestas del simulador de escenarios salariales?
24. ¿Cuál es el costo estimado por día de vacante para posiciones clave según su factor de impacto en la productividad?

### Dominio 6: Planificación de Fuerza Laboral y Productividad
25. ¿Cuál es el tiempo promedio de cobertura de vacantes (*Time-to-Fill*) por departamento y nivel?
26. ¿Cuántos días transcurren desde el ingreso de un colaborador técnico hasta alcanzar su rendimiento esperado (*Time-to-Full Productivity*)?
27. ¿Cuál es la brecha de capacidad proyectada entre la oferta laboral contratada y la demanda operativa en Soporte Clínico?
28. ¿Qué porcentaje de vacantes críticas se cubren mediante promoción interna?

### Dominio 7: Diversidad e Inclusión (DEI)
29. ¿Cuál es la tasa de retención de mujeres en posiciones de liderazgo técnico en comparación con la plantilla general?
30. ¿Cuál es la representación de diversidad en los distintos niveles jerárquicos de la organización?
31. ¿Existen patrones de ausentismo o rotación diferenciados por grupo de antigüedad o rango de edad?

---

## 7. Functional Requirements

### Módulo 1: Ingesta e Integración de Datos
* **FR-01 (HRIS Data Ingestion):** Ingestar datos maestros de colaboradores (demografía, puesto, antigüedad, departamento) para la plantilla activa e histórica.
* **FR-02 (Attendance & Time Logs):** Ingestar registros transaccionales de asistencia, ausencias, licencias y horas extra.
* **FR-03 (Market Intelligence Ingestion):** Ingestar marcadores de mercado (puntos mínimos, medios y máximos salariales) provistos por proveedores externos de inteligencia laboral (*External labor market intelligence providers*).
* **FR-04 (Exit Records Ingestion):** Ingestar registros históricos de desvinculaciones indicando fecha, tipo de término y causa registrada.
* **FR-05 (SLA Events Ingestion):** Ingestar eventos de penalización o incumplimiento de SLA registrados en la operación.

### Módulo 2: Limpieza y Normalización
* **FR-06 (Employee Deduplication):** Identificar y unificar registros de colaboradores mediante un identificador único global.
* **FR-07 (Missing Data Management):** Aplicar reglas de imputación o marcado de banderas para registros incompletos.
* **FR-08 (Currency Standardization):** Convertir valores financieros a Dólares Estadounidenses (USD) utilizando tasas de cambio de referencia.
* **FR-09 (Exit Reason Proxy Analysis):** Reclasificar razones de salida ambiguas mediante el cruce con variables objetivas (salario, horas extra).

### Módulo 3: Analítica de Rotación y Riesgo
* **FR-10 (Turnover Rate Engine):** Calcular la tasa de rotación voluntaria mensual, trimestral y anual acumulada.
* **FR-11 (High-Performer Retention Metric):** Aislar y calcular la tasa de retención exclusiva para personal con desempeño superior (≥ 4/5).
* **FR-12 (Tenure Segmentation):** Agrupar salidas voluntarias por intervalos de antigüedad para identificar momentos críticos de fuga.
* **FR-13 (Flight Risk Score Visualization):** Mostrar en las vistas operativas el nivel de riesgo predictivo de salida por colaborador.
* **FR-14 (Risk Factor Explainability):** Exponer los principales factores individuales que impulsan el riesgo de salida de un colaborador.
* **FR-15 (First-Year Attrition Metric):** Medir el porcentaje de deserciones que ocurren dentro de los primeros 12 meses de servicio.

### Módulo 4: Motor de Ausentismo y Capacidad
* **FR-16 (Bradford Factor Calculation):** Calcular el Factor de Bradford (B = S² × D) por colaborador en ventanas temporales configurables.
* **FR-17 (Absenteeism Categorization):** Clasificar a los colaboradores según los niveles de riesgo de ausentismo parametrizados.
* **FR-18 (Overtime & Absenteeism Analysis):** Evaluar la relación entre la acumulación de horas extra y la frecuencia de ausencias cortas.
* **FR-19 (Capacity Hours Lost):** Cuantificar las horas-hombre de capacidad operativa perdidas por ausentismo no programado.
* **FR-20 (Day-of-Week Pattern Analysis):** Identificar la distribución de ausencias según el día de la semana.

### Módulo 5: Competitividad Salarial y Equidad
* **FR-21 (Compa-Ratio Calculation):** Calcular el *Compa-Ratio* individual comparando el salario base contra el punto medio de mercado.
* **FR-22 (Salary Misalignment Alerts):** Identificar colaboradores de alto desempeño ubicados por debajo de los umbrales de competitividad salarial configurados.
* **FR-23 (Unadjusted Gender Pay Metric):** Calcular la diferencia salarial directa entre géneros por área y nivel.
* **FR-24 (Controlled Pay Gap Analysis):** Emplear modelos estadísticos apropiados para controlar por variables de confusión (experiencia, desempeño, puesto), cuya selección específica se definirá durante la fase analítica tras explorar los datos.
* **FR-25 (Equity Adjustment Budgeting):** Estimación del presupuesto requerido para nivelar salarios a un *Compa-Ratio* objetivo.

### Módulo 6: Impacto Financiero y Costos
* **FR-26 (Turnover Financial Costing):** Calcular el costo total de la rotación sumando costos directos e indirectos de vacancia.
* **FR-27 (SLA Financial Attribution):** Calcular el costo de penalizaciones contractuales atribuibles a déficit de personal en operaciones.
* **FR-28 (Daily Vacancy Cost Engine):** Calcular el costo diario por posición vacante según su factor de impacto productivo.
* **FR-29 (Recruitment Efficiency Savings):** Medir el ahorro por contrataciones directas o internas vs. uso de agencias externas.
* **FR-30 (Net Financial Savings Consolidation):** Consolidar el beneficio financiero neto del proyecto restando la inversión inicial.

### Módulo 7: Modelado Analítico de Factores de Riesgo de Salida y Retención
* **FR-31 (Multifactorial Flight Risk Scoring):** Generar puntuaciones analíticas de riesgo de salida mediante ponderación multivariada de variables de compensación (*Compa-Ratio*), desempeño, sobretiempo acumulado y severidad de ausentismo.
* **FR-32 (Temporal Aggregations & Trend Features):** Calcular variables derivadas de tendencia (acumulado móvil de horas extra en 30 días, Factor de Bradford en 12 meses, historial de cambios salariales).
* **FR-33 (Risk Drivers Decomposition):** Descomponer la contribución relativa de cada factor individual en la puntuación de riesgo del colaborador para orientar la acción del HRBP.
* **FR-34 (Metric Validation & Quality Audit):** Validar la consistencia de las puntuaciones de riesgo calculadas en SQL y Power BI frente a los registros históricos de desvinculaciones.
* **FR-35 (Weight Calibration & Risk Segmentation):** Calibrar ponderaciones y umbrales de segmentación de riesgo para priorizar la identificación de talento crítico en riesgo de fuga.

### Módulo 8: Dashboards Ejecutivos y Simulador
* **FR-36 (Boardroom Overview Screen):** Tablero gerencial consolidado de rotación, ausentismo, SLAs e impacto financiero.
* **FR-37 (HRBP Action Center Screen):** Vista operativa priorizada por nivel de riesgo de salida y causales explicativas.
* **FR-38 (Interactive Financial What-If Simulator):** Simulador de escenarios para ajustar variables de incremento salarial y calcular el ROI neto estimado.
* **FR-39 (Executive Report Export):** Exportación de vistas y reportes en formatos ejecutivos estándar.

### Módulo 9: Seguridad y Gobierno
* **FR-40 (Role-Based Access Control):** Restringir el acceso a datos según el rol y ámbito organizacional del usuario.
* **FR-41 (Data Anonymization & Privacy):** Ocultar datos de identificación personal (PII) en vistas analíticas globales para cumplir normativas de privacidad (RGPD / LATAM).
* **FR-42 (Audit Logging):** Registrar las acciones de consulta y exportación de información sensible.

---

## 8. Non-Functional Requirements (Business Perspective)

* **NFR-PERF-01 (Data Freshness):** Los tableros deben reflejar la información maestra y transaccional actualizada de forma diaria.
* **NFR-PERF-02 (Processing Window):** El procesamiento de la ingesta y cálculo de métricas debe completarse dentro de la ventana nocturna fuera de horario laboral.
* **NFR-PERF-03 (Interactive Responsiveness):** Las consultas e interacciones de usuario en los reportes deben ofrecer tiempos de respuesta fluidos para uso ejecutivo.
* **NFR-SCA-01 (Volume Scalability):** La solución debe admitir el crecimiento de la plantilla hasta 10,000 colaboradores activos sin rediseño funcional.
* **NFR-AVL-01 (Business Availability):** La plataforma debe estar disponible de forma continua durante el horario operativo corporativo.
* **NFR-SEC-01 (Data Protection Standard):** La información sensible de personal debe protegerse mediante estándares de encriptación y seguridad vigentes en reposo y en tránsito *(las especificaciones técnicas exactas se definirán en Architecture.md)*.
* **NFR-SEC-02 (Regulatory Alignment):** Cumplimiento estricto de las normativas de privacidad de datos personales vigentes en Europa (RGPD) y LATAM.
* **NFR-USB-01 (Multilingual Support):** Las interfaces ejecutivas deberán ofrecer soporte bilingüe (Español e Inglés).

---

## 9. Business Rules

### Estatus y Rotación
* **BR-01 (Active Employee):** Colaborador con contrato vigente y sin fecha de egreso efectiva a la fecha de corte.
* **BR-02 (Voluntary Turnover Formula):** 
  `TRV = (Salidas Voluntarias / ((Headcount Inicio + Headcount Fin) / 2)) × 100`
* **BR-03 (High-Performer Definition):** Empleado activo con evaluación de desempeño oficial ≥ 4.0 / 5.0.

### Reglas de Ausentismo (Configurables)
* **BR-06 (Bradford Factor Formula):** B = S² × D, donde S es el número de instancias independientes y D los días totales en 12 meses.
* **BR-07 (Configurable Bradford Thresholds):** Los umbrales del Factor de Bradford serán parámetros configurables por la empresa. Los valores por defecto iniciales se sugieren en:
  * *Bajo:* < 50
  * *Moderado:* 50 - 149
  * *Alerta/Crítico:* 150 - 499
  * *Severo:* ≥ 500
* **BR-08 (Absence Instance):** Cualquier período continuo de ausentismo no programado (1 o más días consecutivos = 1 instancia).
* **BR-09 (Absence Exclusions):** Exclusión de vacaciones reglamentarias, licencias legales y permisos autorizados.

### Reglas de Compensación
* **BR-10 (Compa-Ratio Formula):** 
  `Compa-Ratio = Salario Base Anual (USD) / Punto Medio de Mercado (USD)`
* **BR-11 (Base Salary Scope):** Considera únicamente el salario fijo base pactado, excluyendo bonos variables y horas extra.
* **BR-13 (Market Midpoint Source):** Información salarial actualizada periódicamente a partir de *External labor market intelligence providers*.

### Parámetros Financieros y Operativos
* **BR-14 (SLA Attribution Condition):** Un incumplimiento de SLA se vinculará a déficit de personal cuando la ausencia en el turno supere un porcentaje crítico configurable.
* **BR-15 (SLA Penalty Parameter):** Parámetro estimativo de **$1,200 USD** por evento de incumplimiento imputable a falta de personal.
* **BR-16 (Vacancy Cost Factor):** El costo de vacancia en I+D considera un factor multiplicador configurable de **1.5x** sobre el salario diario cargado.
* **BR-17 (Fully-Loaded Salary Standard):** Incluye salario base más un **30% estimado** por cargas prestacionales y beneficios.
* **BR-20 (Tenure Intervals):** Categorías: `< 6m`, `6-12m`, `1-2a`, `2-5a`, `> 5a`.
* **BR-21 (Overtime Warning Threshold):** Alerta de sobrecarga al acumular más de **30 horas extra** en 30 días.
* **BR-22 (Anonymization Threshold):** Grupos menores a **5 empleados** se consolidarán para proteger la privacidad individual.
* **BR-23 (Proxy Exit Re-classification):** Regla de reclasificación proxy que evalúa salarios bajos (CR < 0.85) o exceso de horas extra (> 30h) para corregir causas de salida genéricas.

---

## 10. Assumptions

1. **Accesibilidad a Fuentes de Datos:** Se asume la disponibilidad periódica de extractos o vistas de los sistemas de RRHH y asistencia.
2. **Validez de Parámetros de Vacancia (1.5x):** Se asume que el multiplicador de vacancia representa una estimación válida de la pérdida de productividad en roles críticos.
3. **Capacidad de Intervención:** Se asume que los HRBPs cuentan con procesos operativos para actuar sobre las alertas de riesgo generadas.
4. **Constancia del Parámetro SLA ($1,200 USD):** Se asume este valor como promedio representativo para el modelado financiero.

---

## 11. Constraints

1. **Restricción Presupuestal:** Presupuesto asignado de **$85,000 USD** para el desarrollo y despliegue del proyecto.
2. **Restricción de Tiempo:** Plazo de ejecución objetivo de **16 semanas** hasta la entrega funcional.
3. **Coexistencia de Sistemas:** La solución complementará y no reemplazará los sistemas transaccionales existentes.

---

## 12. Dependencies

1. Credenciales de acceso a las vistas de información de origen.
2. Entrega de marcadores de mercado salariales por el área de Compensaciones.
3. Validación de las políticas de privacidad y seguridad por los responsables correspondientes.

---

## 13. Acceptance Criteria (Definition of Done)

1. **Procesamiento de Datos:** Ingesta y consolidación sin errores de duplicación sobre los registros de la plantilla en PostgreSQL.
2. **Validación Financiera:** Conformidad de las áreas financieras sobre la estructura de cálculo de costos de vacancia e impacto económico.
3. **Consistencia y Calidad de Métricas:** Cero violaciones de integridad referencial y 100% de reconciliación en cálculos de rotación, ausentismo y compa-ratio entre SQL y DAX.
4. **Disponibilidad de Dashboards:** Vistas operativas y ejecutivas desplegadas con tiempos de respuesta fluidos y control de acceso funcional en Power BI.
5. **Cumplimiento de Privacidad:** Anonimización de información sensible y restricciones de seguridad verificadas.
6. **Paquete de Documentación:** Repositorio en GitHub finalizado con código modularizado y documentación completa de People Analytics.

---

## 14. Traceability Matrix

| Business Objective | Requirement ID | Core Business Metric | Data Source | Primary Dashboard View | Model / Analytics Engine |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Financial Optimization** ($540k Savings) | FR-26, FR-28, FR-30 | Total Turnover Cost ($) / Net Savings | HRIS / Exit / Finance | Boardroom Overview | Financial Cost Engine |
| **High-Performer Retention** | FR-10, FR-11, FR-13, FR-31 | High-Performer Retention Rate (%) | HRIS / Performance / Market | HRBP Action Center | Risk Scoring Engine |
| **SLA Protection** ($0 Penalties) | FR-05, FR-19, FR-27 | SLA Penalty Cost ($) / SLA Rate (%) | Attendance / SLA Log | Boardroom Overview | SLA Attribution Engine |
| **Absenteeism Control** | FR-16, FR-17, FR-18 | Average Bradford Score / Lost Hours | Attendance / Time Log | HRBP Action Center | Bradford Engine |
| **Pay Equity & Merit** | FR-21, FR-24, FR-25, FR-38 | Corporate Compa-Ratio / Adjustment Budget | Salary Bands / HRIS | Financial What-If Simulator | Compa-Ratio Analytics Engine |

---

## 15. Future Enhancements

1. **Análisis de Texto de Salida (v1.0):** Análisis sobre texto libre de comentarios de clima y entrevistas de salida.
2. **Sugerencia de Movilidad Interna (v1.0):** Mapeo de perfiles internos para cubrir vacantes críticas.
3. **Alertas Ejecutivas Automatizadas (v2.0):** Notificaciones periódicas para la alta dirección ante cambios en la exposición financiera de rotación.