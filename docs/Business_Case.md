# Business Case

## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & WORKFORCE DYNAMICS SOLUTION
## MedTech Global Solutions

**Document Version:** v0.3.0  
**Target Audience:** Executive Committee (CFO, CHRO, CIO, VP of Operations)  
**Project Lead:** Emmanuel Rodríguez Mendoza  
**Professional Role:** People Analytics / HR Data Analyst  
**Sponsor:** Head of People Analytics & HR Digital Transformation  
**Date:** 07-29-2026  
**Status:** Submitted for Approval  

---

## 1. Executive Summary

MedTech Global Solutions enfrenta actualmente una amenaza operativa y financiera crítica: una **reducción del 12% en la velocidad de entrega de productos de I+D** y una **exposición inminente de $3.2M USD en renovaciones de contratos B2B de telemedicina**. Esta caída está directamente impulsada por la rotación voluntaria no controlada en el personal clave de I+D y un ausentismo crónico no gestionado en las operaciones de Soporte Clínico en LATAM y Europa.

La iniciativa **Workforce Dynamic Lens** es una solución analítica de People Analytics y Business Intelligence de grado profesional diseñada para mitigar este impacto, transformando la reportería reactiva de RR. HH. en una capacidad analítica diagnóstica con estricto rigor financiero. Mediante la integración de datos del HRIS, registros de asistencia y bandas salariales de mercado en un modelo dimensional en PostgreSQL y dashboards ejecutivos en Power BI, esta solución diagnostica causas raíz de rotación, cuantifica pérdidas en P&L y optimiza la retención de talento crítico.

### Key Financial Highlights
* **Initial Investment Required:** $85,000 USD (Asignación de horas de People Analytics y Data Analytics interno, infraestructura local y desarrollo).
* **Projected 12-Month Gross Savings:** $540,000 USD (Costos de vacancia evitados, reducción de penalizaciones por SLA y optimización de tarifas de reclutamiento).
* **Net Financial Benefit (Year 1):** $455,000 USD.
* **Projected Return on Investment (ROI):** **535%** con un periodo de recuperación de **2.8 meses**.
* **Risk of Inaction:** Pérdidas acumuladas proyectadas superiores a **$3.8M USD** en 12 meses debido a la pérdida de contratos, caída de productividad y rotación en cascada.

---

## 2. Business Context

MedTech Global Solutions opera en un mercado global altamente competitivo, empleando a 4,500 profesionales especializados en ingeniería de software, soporte médico remoto y operaciones regulatorias en LATAM y Europa.

El modelo de ingresos de la empresa depende en gran medida de contratos B2B de telemedicina a largo plazo que exigen el cumplimiento estricto de Acuerdos de Nivel de Servicio (SLAs). Paralelamente, la expansión de productos depende de la velocidad de los ciclos de desarrollo en I+D. En el entorno actual, la retención del talento técnico y la continuidad operativa no son simples métricas de gestión humana: son determinantes directos del margen EBITDA y la valuación corporativa.

---

## 3. Current Situation (As-Is)

La organización gestiona actualmente los datos de personal de manera aislada en sistemas fragmentados:

```text
[ HRIS Local / Hojas de Cálculo ] ──┐
[ Registros de Asistencia/Tiempos ] ──┼─► [ Agregación Manual ] ─► [ Reportes Mensuales Reactivos ]
[ Entrevistas de Salida ] ──────────┘
```

### Critical Operational Bottlenecks:
1. **Lagging Metrics:** RR. HH. reporta la rotación y el ausentismo de forma retroactiva al cierre de mes. Cuando la dirección detecta un pico, el talento ya ha renunciado y las penalizaciones por SLA se han ejecutado.
2. **Qualitative Noise & Exit Interview Bias:** Los datos de salida dependen de opciones genéricas en el HRIS (ej. *"Desarrollo Profesional"*), ocultando las causas reales como la falta de competitividad salarial (*Compa-Ratio*) o la fatiga por horas extra acumuladas.
3. **Financial Disconnect:** La dirección de RR. HH. presenta métricas cualitativas, mientras que Finanzas y Operaciones carecen de visibilidad sobre cómo los días de vacante impactan la velocidad de los proyectos y las penalizaciones contractuales.

---

## 4. Problem Statement

MedTech Global Solutions está sufriendo una erosión financiera silenciosa debido a dos fallas estructurales en la gestión de su capital humano:

1. **High-Performer Flight in R&D:** Ingenieros Senior con alto desempeño (Performance Rating ≥ 4) están renunciando en hitos críticos de los proyectos debido a brechas salariales no monitoreadas frente al mercado. Reemplazar a un Ingeniero Senior requiere entre **60 y 90 días**, periodo en el cual la velocidad de desarrollo cae y se genera sobrecarga en el equipo restante.
2. **Chronic Absenteeism in Clinical Support:** Micro-ausencias no programadas (1 a 2 días) han aumentado drásticamente debido al desgaste por horas extra. Esto genera caídas imprevistas de capacidad operativa, provocando **incumplimientos de SLA** en los contratos con hospitales.

> **Impacto:** De no corregirse, esta dinámica derivará en penalizaciones contractuales continuas, pérdida de clientes clave (cartera B2B de $3.2M USD) y un deterioro severo de la marca empleadora.

---

## 5. Strategic Drivers

Esta iniciativa se alinea directamente con el Plan Estratégico 2026–2028 de MedTech Global Solutions:

* **Operational Excellence:** Restablecer la velocidad de I+D y garantizar un cumplimiento del 99.8% en los SLAs de los contratos B2B.
* **EBITDA Margin Preservation:** Eliminar gastos evitables en agencias externas de reclutamiento, contratistas temporales costosos y penalizaciones contractuales.
* **HR Digital Transformation:** Evolucionar la función de Gestión Humana hacia un socio estratégico de negocio basado en evidencia y datos duros.

---

## 6. Business Opportunity

La solución **Workforce Dynamic Lens** transforma datos operativos y de personal en decisiones de negocio sustentadas:

```text
[ Pipeline Multi-Sistema ] ─► [ Modelo Analítico Dimensional ] ─► [ Acciones Preventivas HRBP ] ─► [ Margen P&L Protegido ]
```

* **Multifactorial Risk Identification:** Análisis multidimensional de retención que cruza brechas salariales (*Compa-Ratio*), sobretiempo y ausentismo para alertar sobre perfiles en riesgo antes de la renuncia formal.
* **Burnout & Capacity Optimization:** El seguimiento estructurado del **Factor de Bradford** aísla el ausentismo crónico por desgaste de las incapacidades médicas legítimas, activando redistribuciones operativas antes de comprometer los SLAs.

---

## 7. Expected Business Benefits

| Benefit Area | Qualitative Impact | Quantitative Target |
| :--- | :--- | :--- |
| **Talent Retention** | Protege la propiedad intelectual y la moral de los equipos en I+D. | **Reducción del 15%** en rotación voluntaria de alto desempeño en 12 meses. |
| **Operational SLA** | Garantiza la cobertura de personal requerida en Soporte Clínico. | **Cero penalizaciones de SLA** atribuibles a falta imprevista de personal. |
| **Time-to-Fill Efficiency** | Agiliza el onboarding y los procesos de selección técnica. | **Reducción del 20%** en el tiempo para alcanzar la máxima productividad. |
| **HR Partner Credibility** | Dota a los HRBPs de argumentos cuantitativos objetivos en comités. | **100% de decisiones** de retención respaldadas en modelos de datos. |

---

## 8. Financial Impact Analysis

### 8.1 Investment Summary (Costs)

| Cost Category | Description | Amount (USD) |
| :--- | :--- | :--- |
| **Internal People Analytics & Data Analytics** | Asignación de horas de People Analytics Lead y Data Analysts | $55,000 |
| **Infrastructure & Data Tools** | Base de datos PostgreSQL, pipelines ETL automatizados en Python y Power BI | $18,000 |
| **Change Management & Training** | Formación a HRBPs y Líderes Operativos en el uso de los dashboards | $12,000 |
| **Total Initial Investment** | | **$85,000** |

### 8.2 Projected Financial Savings (12-Month Horizon)

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ FINANCIAL SAVINGS BREAKDOWN (YEAR 1)                                     │
├──────────────────────────────────────────────────────┬───────────────────┤
│ Costos de vacancia evitados en Talento Clave (I+D)   │ $270,000          │
│ Penalizaciones por incumplimiento de SLA evitadas   │ $110,000           │
│ Reducción en honorarios de agencias de reclutamiento │ $100,000          │
│ Capacidad productiva recuperada (Control ausentismo)│ $60,000            │
├──────────────────────────────────────────────────────┼───────────────────┤
│ TOTAL PROJECTED ANNUAL SAVINGS                       │ $540,000          │
└──────────────────────────────────────────────────────┴───────────────────┘
```

### 8.3 Financial Return Summary

* **Gross Annual Savings:** $540,000 USD
* **Less Initial Investment:** ($85,000 USD)
* **Net Year 1 Financial Benefit:** **$455,000 USD**
* **Return on Investment (ROI):** **535%**
* **Payback Period:** **2.8 Months**

---

## 9. Cost of Inaction (COI)

Optar por no implementar esta solución constituye una decisión financiera con severas pérdidas proyectadas:

```text
Mes 1-3:  Rotación continua de personal clave en I+D  ──► $135,000 USD en costos de reemplazo
Mes 4-6:  Desgaste e incumplimiento de SLAs en Soporte ──► $60,000 USD en penalizaciones directas
Mes 7-12: Pérdida de contratos B2B clave (Telemedicina) ──► $3,200,000 USD en ingresos recurrentes
─────────────────────────────────────────────────────────────────────────────────────────
ESTIMATED 12-MONTH COST OF INACTION: $3,395,000 USD
```

---

## 10. Project Scope

### In-Scope:
* Integración de datos demográficos, desempeño, compensación (*Compa-Ratio*) y antigüedad de 4,500 empleados en LATAM y Europa.
* Procesamiento de logs históricos de asistencia y automatización del cálculo del Factor de Bradford.
* Desarrollo de pipeline ETL en Python/PostgreSQL y vistas analíticas de diagnóstico de rotación.
* Creación de Dashboards Ejecutivos en Power BI con simulador financiero *What-If*.

### Out-of-Scope:
* Reemplazo del sistema HRIS central existente (Workday/BambooHR).
* Modificación automática de nómina sin la aprobación previa del HRBP responsable.
* Análisis de contratistas externos o proveedores de servicios de terceros.

---

## 11. Expected Deliverables

1. **Automated ETL & SQL Analytics Pipeline:** Arquitectura de tablas estrella y vistas optimizadas en PostgreSQL.
2. **Multifactorial Retention Diagnostic Model:** Consultas analíticas y lógicas de segmentación de riesgo basadas en evidencia de RR. HH.
3. **Executive Power BI Dashboard Suite:**
   * *Boardroom Overview Screen:* Indicadores consolidados de rotación, ausentismo e impacto en P&L.
   * *HRBP Action Center:* Análisis diagnóstico individual de riesgo de fuga y brechas salariales.
   * *Financial What-If Simulator:* Cálculo dinámico del ROI según escenarios de ajuste salarial.
4. **Comprehensive Documentation Package:** Repositorio en GitHub con README profesional, Diccionario de Datos y Catálogo de KPIs.

---

## 12. Success Metrics (KPIs)

El desempeño de la iniciativa será evaluado bajo cuatro métricas clave:

1. **High-Performer Retention Rate:** Incrementar la retención de personal de alto desempeño (≥ 4/5) en I+D a un nivel **≥ 90%**.
2. **Average Bradford Score:** Reducir la severidad del ausentismo en Soporte Clínico de **> 150** (zona de riesgo) a **< 85** (rango normal).
3. **Metric Integrity & Reconciliation:** Garantizar **0 violaciones de integridad referencial** y 100% de consistencia entre datos de base de datos y Power BI.
4. **Financial Realization:** Lograr un ahorro neto auditado mínimo de **$300,000 USD** al cierre del ejercicio 2027.

---

## 13. Risk Management Matrix

| Identified Risk | Severity | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Data Quality & HRIS Noise:** Causas de salida mal registradas por los líderes. | Alta | Alta | Utilizar variables proxy objetivas (*Compa-Ratio*, horas extra, antigüedad) junto con el texto de salida. |
| **Data Privacy (GDPR/LATAM):** Manejo de información sensible. | Alta | Media | Implementar anonimización de datos, control de acceso basado en roles (RBAC) y seguridad a nivel de fila. |
| **HRBP Adoption Resistance:** HRBPs escépticos ante nuevas herramientas analíticas. | Media | Media | Capacitación práctica posicionando la herramienta como un asistente de decisión para fundamentar planes de retención. |

---

## 14. Key Project Assumptions

* **Vacancy Cost Factor:** Cada día que una posición Senior en I+D permanece vacante cuesta 1.5 veces el salario diario del rol debido a la pérdida de velocidad y la redistribución de tareas.
* **SLA Penalty Rate:** Se establece un costo penal estimado de **$1,200 USD** por cada evento de incumplimiento de SLA atribuible a falta de personal en Soporte Clínico.
* **Data Access:** Los equipos de IT y Datos facilitarán credenciales de lectura a las tablas del HRIS dentro de los 10 días hábiles posteriores a la aprobación del proyecto.

---

## 15. Alternatives Considered

```text
┌───────────────────────────┬─────────────────────────────┬──────────────────────────────────────────┐
│ Alternative               │ Projected Cost              │ Decision & Rationale                     │
├───────────────────────────┼─────────────────────────────┼──────────────────────────────────────────┤
│ Option A: Status Quo      │ $0 Inicial / $3.4M Riesgo   │ RECHAZADA. Pérdidas financieras continuas│
│ Option B: External Agency │ $250,000 USD                │ RECHAZADA. Costo elevado y poca adopción │
│ Option C: Off-the-Shelf   │ $120,000 USD/año recurrente │ RECHAZADA. Rigidez para adaptar reglas   │
│ Enterprise SaaS Module    │                             │ de SLA y Factor de Bradford locales.     │
│ Option D: In-House Build  │ $85,000 USD Pago Único      │ RECOMENDADA. Máximo ROI, flexibilidad    │
│ (Workforce Dynamic Lens)  │                             │ total y propiedad del código e insights. │
└───────────────────────────┴─────────────────────────────┴──────────────────────────────────────────┘
```

---

## 16. Final Recommendation

El Equipo Técnico de People Analytics recomienda al Comité Ejecutivo **aprobar la asignación presupuestal de $85,000 USD** para el desarrollo e implementación inmediata de la plataforma **Workforce Dynamic Lens**.

Con esta aprobación, MedTech Global Solutions protegerá su cartera de ingresos B2B de $3.2M USD, recuperará la capacidad de ejecución en I+D y establecerá una arquitectura de datos sólida y escalable para la gestión de su capital humano.

---

## 17. Executive Sign-Off & Approval Request

```text
[✓] APPROVED FOR IMMEDIATE IMPLEMENTATION

Emmanuel Rodríguez Mendoza
People Analytics / HR Data Analyst
MedTech Global Solutions
```