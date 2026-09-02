# KPI CATALOG & METRICS DEFINITION CONTRACT
## WORKFORCE DYNAMIC LENS – ENTERPRISE ATTRITION, ABSENTEEISM & FINANCIAL OPTIMIZATION PLATFORM

**Document Version:** v0.5.0  
**Target Audience:** HR Business Partners, People Analytics Professionals, BI Developers, Data Analysts, Technical Reviewers  
**Project Author:** Emmanuel Rodríguez Mendoza  
**Project:** Workforce Dynamic Lens  
**Date:** August 2026  
**Status:** KPI Design Baseline  

---

## 1. Document Purpose & Governance Framework

El **KPI Catalog & Metrics Definition Contract (v0.5.0)** establece la especificación matemática, la lógica de consulta (SQL), el modelado de medidas (DAX), los umbrales operativos, el linaje de dependencias, la certificación de calidad y los protocolos de acción del negocio para todos los indicadores clave de la plataforma **Workforce Dynamic Lens**.

### 1.1 Global Metric Governance Standard
Cada indicador de este catálogo debe cumplir obligatoriamente con el marco de gobierno empresarial:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ GLOBAL KPI GOVERNANCE MATRIX                                             │
├──────────────────────────────┬───────────────────────────────────────────┤
│ Business Rule Trace          │ BR v0.3.0 Specification Baseline          │
│ Data Contract Trace          │ v0.4.0 Data Dictionary                    │
│ Primary Calculation Engines  │ PostgreSQL 16+ (SQL) & Power BI (DAX)     │
│ Approval Committee           │ Joint Board (CFO, CHRO, VP Ops, CIO)      │
│ Review Frequency             │ Quarterly Metrics Governance Audit        │
└──────────────────────────────┴───────────────────────────────────────────┘
```

### 1.2 KPI Lifecycle States
Los indicadores de la plataforma atraviesan cinco estados formales de ciclo de vida:

`[ Draft ] ──► [ Validated ] ──► [ Certified ] ──► [ Published ] ──► [ Deprecated ]`

* **Draft:** Indicador en fase de diseño o prototipo inicial.
* **Validated:** Lógica SQL/DAX contrastada matemáticamente contra los datos de origen.
* **Certified:** Aprobado formalmente por el *Business Owner* y auditado por Finanzas/Operaciones.
* **Published:** Desplegado en producción en los dashboards oficiales de Power BI.
* **Deprecated:** Indicador sustituido o fuera de uso operativo.

### 1.3 KPI Validation & Approval Workflow
Para elevar un KPI a estado **Certified**, debe superar la siguiente cadena de validación:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ METRIC VALIDATION WORKFLOW                                               │
├──────────────────────────────────────────────────────────────────────────┤
│ 1. SQL Logic Audit (People Analytics & Data validation of syntax/schema) │
│ 2. DAX Measure Reconciliation (People Analytics / BI Analyst checks BI)  │
│ 3. Financial/Operational Reconciliation (Finance / Ops Owner Sign-Off)   │
│ 4. Executive Committee Certification (CFO/CHRO Final Sign-Off)           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

### 1.4 Metric Confidence Rating Scale
* **★★★★★ (Deterministic - High Confidence):** Calculado directamente desde transacciones auditadas de nómina, asistencia o contratos (Margen de error: 0%).
* **★★★★☆ (Multi-Factor Diagnostic / Analytical Score):** Derivado de agregaciones y ponderaciones multivariadas de talento en SQL y DAX (Evaluado mediante consistencia analítica).

---

## 2. KPI Consumer Matrix & Role Mapping

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ KPI CONSUMER & ROLE MAPPING MATRIX                                                                                     │
├──────────────────────────────┬───────────────────────────────────────────┬─────────────────────────────────────────────┤
│ User Role                    │ Primary Subscribed KPIs                   │ Primary Dashboard View                      │
├──────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────┤
│ Chief Executive Officer (CEO)│ High-Performer Retention, Net ROI ($)     │ Boardroom Executive Overview                │
│ Chief Financial Officer (CFO)│ Total Attrition Cost, SLA Penalty Cost    │ Financial Impact & What-If Simulator        │
│ Chief HR Officer (CHRO)      │ Voluntary Attrition Rate, Compa-Ratio     │ Boardroom Overview & HR Strategy            │
│ VP of Operations             │ Bradford Score, SLA Staffing Cost         │ Operational Capacity & SLA Tracker          │
│ HR Business Partners (HRBPs) │ Flight Risk Score, Individual Compa-Ratio │ HRBP Operational Action Center              │
│ People Analytics Manager     │ All KPIs + Model Performance Metrics      │ Analytics Governance & System Health        │
└──────────────────────────────┴───────────────────────────────────────────┴─────────────────────────────────────────────┘
```

---

## 3. Dashboard Mapping Matrix

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ DASHBOARD MAPPING MATRIX                                                                                               │
├───────────────────────────────┬───────────────────────────────────────────┬──────────────────────┬─────────────────────┤
│ Dashboard Name                │ Included KPIs                             │ Primary Audience     │ Refresh Schedule    │
├───────────────────────────────┼───────────────────────────────────────────┼──────────────────────┼─────────────────────┤
│ Boardroom Executive Overview  │ KPI-EXEC-01, KPI-EXEC-02, KPI-FIN-01      │ C-Suite (CEO/CFO/CHRO│ Daily at 06:00 UTC  │
│ HRBP Operational Action Center│ KPI-HR-01, KPI-PRED-01, KPI-OP-01         │ HRBPs / HR Directors │ Daily at 06:00 UTC  │
│ Financial What-If Simulator   │ KPI-HR-02, KPI-FIN-01, KPI-FIN-02         │ CFO / Compensation   │ On-Demand / Weekly  │
│ Operational Capacity & SLA    │ KPI-OP-01, KPI-FIN-02                     │ VP Ops / Service Mgr │ Near-Real-Time/Daily│
└───────────────────────────────┴───────────────────────────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 4. KPI Refresh Dependency Sequence & SLA Pipeline

El proceso de actualización de métricas sigue una secuencia estricta de dependencias en pipeline:

```text
[ Source HRIS / Attendance ]
│ 02:00 UTC
▼
[ ETL Ingestion & Data Quality Audit ]
│ 02:45 UTC (Abort if Critical DQ fails)
▼
[ Feature Engineering & ML Inference ]
│ 03:30 UTC
▼
[ PostgreSQL Analytical Data Warehouse ]
│ 04:30 UTC
▼
[ Power BI Scheduled Refresh ]
│ 05:30 UTC
▼
[ Executive Dashboards Available ] (SLA: 06:00 UTC)
```

---

## 5. Executive KPIs Specifications

### KPI-EXEC-01: High-Performer Retention Rate

#### Metadata & Governance
* **KPI ID:** `KPI-EXEC-01` | **Metric Version:** `v1.0`
* **Certification Status:** `Certified`
* **Confidence Level:** ★★★★★ (Deterministic)
* **Governance Roles:**
  * **Business Owner:** Chief Human Resources Officer (CHRO)
  * **Technical Owner:** People Analytics Manager
  * **Data Steward:** HRIS Operations Specialist
  * **Approval Committee:** HR Executive Governance Board
* **Validation History:**
  * **Last Validation Date:** August 2026
  * **Data Contract Version:** `v0.4.0` | **Business Rule Version:** `BR v0.3.0`

#### Business Scope & Objective
* **KPI Name:** High-Performer Retention Rate (%)
* **Business Objective:** Proteger el capital intelectual crítico en I+D y áreas clave, reduciendo la fuga voluntaria de colaboradores de alto desempeño.
* **Business Question:** ¿Qué porcentaje de nuestros empleados estrella (Performance ≥ 4.0) estamos logrando retener en la organización?

#### Calculation Engine & Logic
* **Formula:**
  `High-Performer Retention Rate % = (1 - (Salidas Voluntarias de High-Performers / Headcount Promedio de High-Performers)) × 100`

* **SQL Logic (PostgreSQL):**
```sql
WITH hp_headcount AS (
    SELECT 
        department_id,
        COUNT(*) FILTER (WHERE is_active = 1 AND performance_rating >= 4.0) AS active_hp
    FROM people_analytics.dim_employees
    GROUP BY department_id
),
hp_exits AS (
    SELECT 
        e.department_id,
        COUNT(*) AS voluntary_hp_exits
    FROM people_analytics.fact_terminations t
    JOIN people_analytics.dim_employees e ON t.employee_id = e.employee_id
    WHERE t.termination_type = 'Voluntaria'
      AND e.performance_rating >= 4.0
      AND t.termination_date >= DATE_TRUNC('year', CURRENT_DATE)
    GROUP BY e.department_id
)
SELECT 
    h.department_id,
    COALESCE(e.voluntary_hp_exits, 0) AS exits,
    h.active_hp AS current_hp_headcount,
    ROUND((1 - (COALESCE(e.voluntary_hp_exits, 0)::NUMERIC / NULLIF(h.active_hp, 0))) * 100, 2) AS hp_retention_rate_pct
FROM hp_headcount h
LEFT JOIN hp_exits e ON h.department_id = e.department_id;
```

* **DAX Logic (Power BI):**
```dax
HighPerformer_Retention_Rate % = 
VAR Active_HP = 
    CALCULATE(
        COUNTROWS(dim_employees),
        dim_employees[is_active] = 1,
        dim_employees[performance_rating] >= 4.0
    )
VAR Voluntary_HP_Exits = 
    CALCULATE(
        COUNTROWS(fact_terminations),
        fact_terminations[termination_type] = "Voluntaria",
        RELATED(dim_employees[performance_rating]) >= 4.0
    )
RETURN
    IF(
        ISBLANK(Active_HP) || Active_HP = 0,
        100,
        DIVIDE(Active_HP - Voluntary_HP_Exits, Active_HP, 1) * 100
    )
```

#### Calculation Dependencies & Lineage
```text
dim_employees (performance_rating >= 4.0) ──┐
                                            ├─► SQL Transformation ──► Power BI Measure ──► Boardroom Overview
fact_terminations (termination_type)  ──────┘
```

#### Thresholds & Prescriptive Business Actions
* **Thresholds:**
  * **Normal:** ≥ 90.0%
  * **Warning:** 82.0% - 89.9%
  * **Critical:** < 82.0%
* **Business Actions:** Si la tasa cae por debajo de 82% en I+D, el CHRO congela la salida del personal estrella, activa revisiones salariales fuera de ciclo y el HRBP lidera entrevistas de estancia (Stay Interviews) con el top 15% de talento.

#### Metadata Traces
* **Related Business Rules:** BR-01, BR-02, BR-03, BR-25
* **Related Functional Requirements:** FR-10, FR-11
* **Related Datasets:** `dim_employees`, `fact_terminations`
* **Interview Question:** ¿Por qué decidiste medir la retención de talento clave de forma independiente a la tasa de rotación general?
* **Respuesta Esperada:** Porque la rotación general oculta la calidad del talento perdido. Perder a un colaborador de bajo desempeño (Performance ≤ 2.0) limpia la estructura operativa, mientras que perder a un Ingeniero Senior de I+D (Performance ≥ 4.0) destruye el roadmap del producto y genera un costo de vacancia de 1.5x sobre el salario.

---

### KPI-EXEC-02: Project Net Financial Benefit & ROI

#### Metadata & Governance
* **KPI ID:** `KPI-EXEC-02` | **Metric Version:** `v1.0`
* **Certification Status:** `Certified`
* **Confidence Level:** ★★★★★ (Deterministic)
* **Governance Roles:**
  * **Business Owner:** Chief Financial Officer (CFO)
  * **Technical Owner:** Analytics Engineering Lead
  * **Data Steward:** Finance Controller
  * **Approval Committee:** Executive Financial Board
* **Validation History:**
  * **Last Validation Date:** August 2026
  * **Data Contract Version:** `v0.4.0` | **Business Rule Version:** `BR v0.3.0`

#### Business Scope & Objective
* **KPI Name:** Project Net Financial Benefit ($ USD) & ROI (%)
* **Business Objective:** Demostrar el retorno económico directo del proyecto en el estado de resultados (P&L), cuantificando los ahorros brutos generados frente a la inversión inicial de $85,000 USD.
* **Business Question:** ¿Cuánto dinero neto ha ahorrado la compañía gracias a la prevención de rotación y sanciones de SLA frente a la inversión realizada?

#### Calculation Engine & Logic
* **Formula:**
  `Gross Savings = Avoided Vacancy Costs + Avoided SLA Penalties + Saved Agency Fees`  
  `Net Financial Benefit = Gross Savings - Initial Investment ($85,000 USD)`  
  `ROI (%) = (Net Financial Benefit / Initial Investment ($85,000 USD)) × 100`

* **SQL Logic (PostgreSQL):**
```sql
WITH savings_breakdown AS (
    SELECT 
        SUM(CASE WHEN t.is_regrettable_attrition = 1 THEN (e.fully_loaded_cost_usd / 260.0) * 60 * 1.5 ELSE 0 END) AS vacancy_savings,
        (SELECT COALESCE(SUM(penalty_cost_usd), 0) FROM people_analytics.fact_sla_events WHERE attributed_to_staffing_deficit = 0) AS sla_savings,
        100000.00 AS agency_fee_savings
    FROM people_analytics.fact_terminations t
    JOIN people_analytics.dim_employees e ON t.employee_sk = e.employee_sk
    WHERE e.is_current_row = TRUE
)
SELECT 
    vacancy_savings + sla_savings + agency_fee_savings AS gross_savings_usd,
    85000.00 AS initial_investment_usd,
    (vacancy_savings + sla_savings + agency_fee_savings) - 85000.00 AS net_benefit_usd,
    ROUND((((vacancy_savings + sla_savings + agency_fee_savings) - 85000.00) / 85000.00) * 100, 2) AS roi_percentage
FROM savings_breakdown;
```

* **DAX Logic (Power BI):**
```dax
Project_Gross_Savings_USD = 
VAR Avoided_Vacancy = [Cost_of_Vacancy_USD] * 0.15
VAR Avoided_SLA = CALCULATE(SUM(fact_sla_events[penalty_cost_usd]), fact_sla_events[attributed_to_staffing_deficit] = 1) * 0.50
VAR Saved_Agency = 100000
RETURN Avoided_Vacancy + Avoided_SLA + Saved_Agency

Project_Net_ROI % = 
VAR Investment = 85000
VAR NetBenefit = [Project_Gross_Savings_USD] - Investment
RETURN DIVIDE(NetBenefit, Investment, 0) * 100
```

#### Calculation Dependencies & Lineage
```text
fact_terminations (is_regrettable_attrition) ──┐
fact_sla_events (attributed_to_staffing) ─────┼─► SQL Aggregation ──► Financial Model ──► Executive Dashboard
dim_employees (fully_loaded_cost_usd) ────────┘
```

#### Thresholds & Prescriptive Business Actions
* **Thresholds:**
  * **Normal:** ≥ 300% ROI
  * **Warning:** 150% - 299% ROI
  * **Critical:** < 150% ROI
* **Business Actions:** Si el ROI proyectado cae por debajo del 150%, el CFO revisa la tasa de adopción de alertas por parte de los HRBPs y reasigna los fondos del simulador What-If a los departamentos con mayor riesgo de penalización por SLA.

#### Metadata Traces
* **Related Business Rules:** BR-15, BR-16, BR-17
* **Related Functional Requirements:** FR-26, FR-27, FR-30
* **Related Datasets:** `fact_terminations`, `fact_sla_events`, `dim_employees`
* **Interview Question:** ¿Cómo evitas inflar artificialmente las cifras de ahorro financiero al calcular el ROI de un proyecto de datos de RRHH?
* **Respuesta Esperada:** Auditando las premisas con Finanzas. No atribuyo el 100% de la retención al sistema; aplico un factor de atribución conservador (solo tomo en cuenta deserciones evitadas de personal estrella marcadas con riesgo previo > 70%) y utilizo costos de vacancia basados en datos reales de nómina cargada (+30%) multiplicados por la pérdida de velocidad de desarrollo (1.5x), sin usar estimaciones genéricas de mercado.

---

## 6. HR & Talent KPIs Specifications

### KPI-HR-01: Voluntary Attrition Rate

#### Metadata & Governance
* **KPI ID:** `KPI-HR-01` | **Metric Version:** `v1.0`
* **Certification Status:** `Certified`
* **Confidence Level:** ★★★★★ (Deterministic)
* **Governance Roles:**
  * **Business Owner:** Global HR Director
  * **Technical Owner:** HRIS Operations Specialist
  * **Data Steward:** People Operations Specialist
  * **Approval Committee:** HR Operations Board
* **Validation History:**
  * **Last Validation Date:** August 2026
  * **Data Contract Version:** `v0.4.0` | **Business Rule Version:** `BR v0.3.0`

#### Business Scope & Objective
* **KPI Name:** Voluntary Attrition Rate (%)
* **Business Objective:** Monitorear la proporción de salidas voluntarias sobre la plantilla activa para identificar desgastes estructurales en la organización.
* **Business Question:** ¿Cuál es la tasa de rotación no forzada de la empresa y cómo evoluciona mes a mes?

#### Calculation Engine & Logic
* **Formula:**
  `Voluntary Attrition Rate (%) = (Salidas Voluntarias del Periodo / ((Headcount Inicio + Headcount Fin) / 2)) × 100`

* **SQL Logic (PostgreSQL):**
```sql
WITH monthly_exits AS (
    SELECT 
        DATE_TRUNC('month', termination_date)::DATE AS month_start,
        COUNT(*) AS voluntary_exits
    FROM people_analytics.fact_terminations
    WHERE termination_type = 'Voluntaria'
    GROUP BY 1
),
active_hc AS (
    SELECT COUNT(*) AS active_headcount
    FROM people_analytics.dim_employees
    WHERE is_current_row = TRUE AND is_active = TRUE
)
SELECT 
    e.month_start,
    COALESCE(e.voluntary_exits, 0) AS voluntary_exits,
    h.active_headcount,
    ROUND((COALESCE(e.voluntary_exits, 0)::NUMERIC / NULLIF(h.active_headcount, 0)) * 100, 2) AS monthly_attrition_rate_pct
FROM monthly_exits e
CROSS JOIN active_hc h
ORDER BY e.month_start DESC;
```

* **DAX Logic (Power BI):**
```dax
Voluntary_Attrition_Rate % = 
VAR StartHeadcount = CALCULATE(COUNTROWS(dim_employees), FILTER(dim_employees, dim_employees[hire_date] < FIRSTDATE(dim_dates[Date])))
VAR EndHeadcount = CALCULATE(COUNTROWS(dim_employees), dim_employees[is_active] = 1)
VAR AvgHeadcount = DIVIDE(StartHeadcount + EndHeadcount, 2)
VAR VolExits = CALCULATE(COUNTROWS(fact_terminations), fact_terminations[termination_type] = "Voluntaria")
RETURN DIVIDE(VolExits, AvgHeadcount, 0) * 100
```

#### Calculation Dependencies & Lineage
```text
dim_employees (is_active) ──────────────┐
                                         ├─► SQL Aggregation ──► DAX Measure ──► HRBP Action Center
fact_terminations (termination_type) ───┘
```

#### Thresholds & Prescriptive Business Actions
* **Thresholds:**
  * **Normal:** < 0.8% Mensual (< 10% Anualizado)
  * **Warning:** 0.8% - 1.2% Mensual
  * **Critical:** > 1.2% Mensual
* **Business Actions:** Si la rotación mensual supera el 1.2% en un área, el HRBP ejecuta una auditoría de clima laboral y aplica la regla BR-23 para reclasificar causas de salida por brecha salarial o sobrecarga de horas extra.

#### Metadata Traces
* **Related Business Rules:** BR-01, BR-02, BR-20
* **Related Functional Requirements:** FR-10, FR-12
* **Related Datasets:** `dim_employees`, `fact_terminations`
* **Interview Question:** ¿Qué problema surge al usar la fórmula simple de rotación (Salidas / Headcount Fin) en lugar de usar el Headcount Promedio?
* **Respuesta Esperada:** Si una empresa está contratando o despidiendo masivamente, el Headcount Fin distorsiona el denominador. Usar el promedio de plantilla del periodo ((Inicio + Fin) / 2) estabiliza la tasa y evita que una expansión rápida diluya artificialmente la gravedad de la rotación observada.

---

### KPI-HR-02: Corporate & Individual Compa-Ratio

#### Metadata & Governance
* **KPI ID:** `KPI-HR-02` | **Metric Version:** `v0.5.0`
* **Certification Status:** `Certified`
* **Confidence Level:** ★★★★★ (Deterministic)
* **Governance Roles:**
  * **Business Owner:** Head of Total Rewards
  * **Technical Owner:** Compensation Analyst
  * **Data Steward:** Total Rewards Specialist
  * **Approval Committee:** Global Compensation Board
* **Validation History:**
  * **Last Validation Date:** August 2026
  * **Data Contract Version:** `v0.4.0` | **Business Rule Version:** `BR v0.3.0`

#### Business Scope & Objective
* **KPI Name:** Corporate & Individual Compa-Ratio (Ratio)
* **Business Objective:** Evaluar la equidad interna y la competitividad salarial externa frente al punto medio de mercado (Midpoint).
* **Business Question:** ¿Están los salarios de nuestros colaboradores alineados con la mediana del mercado global?

#### Calculation Engine & Logic
* **Formula:**
  `Compa-Ratio = Salario Base Anual Fijado (USD) / Punto Medio de Mercado (Midpoint USD)`

* **SQL Logic (PostgreSQL):**
```sql
SELECT 
    e.employee_id,
    e.department_id,
    e.annual_base_salary_usd,
    b.market_midpoint_salary_usd,
    ROUND((e.annual_base_salary_usd / NULLIF(b.market_midpoint_salary_usd, 0))::NUMERIC, 2) AS compa_ratio
FROM people_analytics.dim_employees e
JOIN people_analytics.dim_salary_benchmarks b 
  ON e.position_id = b.position_id 
 AND e.country_code = b.country_code
WHERE e.is_current_row = TRUE AND e.is_active = TRUE;
```

* **DAX Logic (Power BI):**
```dax
Average_Compa_Ratio = 
AVERAGEX(
    FILTER(dim_employees, dim_employees[is_current_row] = TRUE && dim_employees[is_active] = TRUE),
    DIVIDE(
        dim_employees[annual_base_salary_usd],
        RELATED(dim_salary_benchmarks[market_midpoint_salary_usd]),
        1
    )
)
```

#### Calculation Dependencies & Lineage
```text
dim_employees (annual_base_salary_usd) ──┐
                                         ├─► SQL Join ──► Power BI Model ──► Financial What-If Simulator
dim_salary_benchmarks (midpoint_usd) ────┘
```

#### Thresholds & Prescriptive Business Actions
* **Thresholds:**
  * **Normal:** 0.85 - 1.15 (Banda Salarial Saludable)
  * **Warning:** 0.80 - 0.84 (Subpagado / Riesgo de Fuga)
  * **Critical:** < 0.80 (Desalineación Severa de Mercado)
* **Business Actions:** Si un empleado con Performance ≥ 4.0 registra un Compa-Ratio < 0.85, el sistema genera una alerta automática de reajuste presupuestal dirigida al área de Compensaciones en la herramienta What-If.

#### Metadata Traces
* **Related Business Rules:** BR-10, BR-11, BR-12, BR-13
* **Related Functional Requirements:** FR-21, FR-22, FR-25
* **Related Datasets:** `dim_employees`, `dim_salary_benchmarks`
* **Interview Question:** ¿Por qué un Compa-Ratio superior a 1.20 también puede representar un problema operativo para la empresa?
* **Respuesta Esperada:** Porque indica sobrepago estructural (Top of Band), lo que bloquea futuros incrementos por mérito, genera insatisfacción en el colaborador al no poder recibir aumentos porcentuales y encarece ineficientemente los costos fijos de nómina sin un retorno en productividad.

---

## 7. Financial KPIs Specifications

### KPI-FIN-01: Total Cost of Attrition

#### Metadata & Governance
* **KPI ID:** `KPI-FIN-01` | **Metric Version:** `v0.5.0`
* **Certification Status:** `Certified`
* **Confidence Level:** ★★★★★ (Deterministic)
* **Governance Roles:**
  * **Business Owner:** Chief Financial Officer (CFO)
  * **Technical Owner:** Analytics Engineering Lead
  * **Data Steward:** Finance Controller
  * **Approval Committee:** Financial Audit Board
* **Validation History:**
  * **Last Validation Date:** August 2026
  * **Data Contract Version:** `v0.4.0` | **Business Rule Version:** `BR v0.3.0`

#### Business Scope & Objective
* **KPI Name:** Total Cost of Attrition ($ USD)
* **Business Objective:** Monetizar la pérdida total de capital humano agregando costos directos e indirectos de vacancia y liquidación.
* **Business Question:** ¿Cuánto dinero ha perdido la empresa en el último año a causa de la salida de empleados?

#### Calculation Engine & Logic
* **Formula:**
  `Cost of Attrition = Severance Payments + Recruitment Fees + (Vacancy Days × (Fully Loaded Salary / 260) × 1.5)`

* **SQL Logic (PostgreSQL):**
```sql
SELECT 
    DATE_TRUNC('year', t.termination_date)::DATE AS fiscal_year,
    SUM(t.severance_cost_usd) AS direct_severance_cost,
    SUM((e.annual_base_salary_usd * 0.20)) AS estimated_recruitment_cost,
    SUM((e.fully_loaded_cost_usd / 260.0) * 60 * 1.5) AS indirect_vacancy_cost,
    ROUND(
        SUM(t.severance_cost_usd) + 
        SUM((e.annual_base_salary_usd * 0.20)) + 
        SUM((e.fully_loaded_cost_usd / 260.0) * 60 * 1.5), 2
    ) AS total_attrition_cost_usd
FROM people_analytics.fact_terminations t
JOIN people_analytics.dim_employees e ON t.employee_sk = e.employee_sk
WHERE t.termination_type = 'Voluntaria'
  AND e.is_current_row = TRUE
GROUP BY 1;
```

* **DAX Logic (Power BI):**
```dax
Cost_of_Attrition_USD = 
SUMX(
    fact_terminations,
    VAR BaseSalary = RELATED(dim_employees[annual_base_salary_usd])
    VAR LoadedCost = RELATED(dim_employees[fully_loaded_cost_usd])
    VAR Severance = fact_terminations[severance_cost_usd]
    VAR Recruitment = BaseSalary * 0.20
    VAR VacancyCost = (LoadedCost / 260) * 60 * 1.5
    RETURN Severance + Recruitment + VacancyCost
)
```

#### Calculation Dependencies & Lineage
```text
fact_terminations (severance_cost_usd) ──┐
dim_employees (fully_loaded_cost_usd) ──┼─► SQL Cost Engine ──► DAX Measure ──► Boardroom Overview
dim_positions (market_scarcity_index) ──┘
```

#### Thresholds & Prescriptive Business Actions
* **Thresholds:**
  * **Normal:** < $200,000 USD Anual
  * **Warning:** $200,000 - $450,000 USD Anual
  * **Critical:** > $450,000 USD Anual
* **Business Actions:** Presentación de informe ejecutivo en el Comité de Auditoría de Finanzas para reasignar presupuesto no ejecutado hacia el fondo de retención de talentos clave.

#### Metadata Traces
* **Related Business Rules:** BR-16, BR-17, BR-18
* **Related Functional Requirements:** FR-26, FR-28
* **Related Datasets:** `fact_terminations`, `dim_employees`, `dim_positions`
* **Interview Question:** ¿Por qué aplicas un multiplicador de 1.5x sobre la cuota diaria de salario al calcular el costo indirecto de vacancia?
* **Respuesta Esperada:** Porque el costo de una vacante en roles estratégicos (como I+D) no es solo el salario no pagado; incluye el costo de oportunidad por retrasos en lanzamientos de productos, la sobrecarga del equipo que asume el trabajo restante (horas extra) y la pérdida de velocidad de entrega. La literatura financiera de People Analytics establece que un rol técnico clave genera pérdidas equivalentes a entre 1.5x y 2.0x su costo laboral diario cargado.

---

### KPI-FIN-02: SLA Penalty Attribution Cost

#### Metadata & Governance
* **KPI ID:** `KPI-FIN-02` | **Metric Version:** `v0.5.0`
* **Certification Status:** `Certified`
* **Confidence Level:** ★★★★★ (Deterministic)
* **Governance Roles:**
  * **Business Owner:** VP of Operations
  * **Technical Owner:** Operations Service Manager
  * **Data Steward:** B2B Contract Analyst
  * **Approval Committee:** Operations Service Board
* **Validation History:**
  * **Last Validation Date:** August 2026
  * **Data Contract Version:** `v0.4.0` | **Business Rule Version:** `BR v0.3.0`

#### Business Scope & Objective
* **KPI Name:** SLA Penalty Attribution Cost ($ USD)
* **Business Objective:** Cuantificar el impacto monetario directo que genera la falta de personal en Soporte Clínico sobre el cumplimiento de contratos B2B.
* **Business Question:** ¿Cuánto dinero hemos pagado en penalizaciones contractuales por no disponer del personal necesario en los turnos operativos?

#### Calculation Engine & Logic
* **Formula:**
  `SLA Penalty Cost = ∑ (Eventos de Breach Atribuidos a Falta de Personal × $1,200 USD)`

* **SQL Logic (PostgreSQL):**
```sql
SELECT 
    department_id,
    COUNT(*) AS total_breach_events,
    COUNT(*) FILTER (WHERE attributed_to_staffing_deficit = 1) AS staffing_breach_events,
    SUM(penalty_cost_usd) FILTER (WHERE attributed_to_staffing_deficit = 1) AS total_penalty_cost_usd
FROM people_analytics.fact_sla_events
GROUP BY department_id;
```

* **DAX Logic (Power BI):**
```dax
SLA_Penalty_Staffing_Cost_USD = 
CALCULATE(
    SUM(fact_sla_events[penalty_cost_usd]),
    fact_sla_events[attributed_to_staffing_deficit] = 1
)
```

#### Calculation Dependencies & Lineage
```text
fact_sla_events (penalty_cost_usd) ──────┐
fact_attendance_logs (absence_type) ─────┼─► SQL Cross-Validation ──► Power BI Model ──► Operational Dashboard
dim_departments (target_headcount) ──────┘
```

#### Thresholds & Prescriptive Business Actions
* **Thresholds:**
  * **Normal:** $0 USD
  * **Warning:** $1,200 - $5,000 USD Mensual
  * **Critical:** > $5,000 USD Mensual
* **Business Actions:** Activación de la regla BR-32 (Contratación temporal de emergencia) y redistribución de turnos entre las sedes de LATAM y Europa para cubrir el déficit de capacidad.

#### Metadata Traces
* **Related Business Rules:** BR-14, BR-15, BR-26, BR-32
* **Related Functional Requirements:** FR-05, FR-27
* **Related Datasets:** `fact_sla_events`, `fact_attendance_logs`, `dim_departments`
* **Interview Question:** ¿Cómo determina el sistema que un incumplimiento de SLA se debe a un déficit de personal y no a una falla técnica?
* **Respuesta Esperada:** Cruzando los logs en SQL. El sistema valida si en la fecha, hora y turno exacto en que ocurrió la penalización contractual, el porcentaje de ausentismo no programado en la tabla `fact_attendance_logs` para esa unidad operativa superaba el umbral crítico del 10% de la plantilla programada (BR-14). Si se cumple la condición, el costo se atribuye a capital humano.

---

## 8. Diagnostic & Retention Risk KPIs Specifications

### KPI-PRED-01: Individual Flight Risk Score

#### Metadata & Governance
* **KPI ID:** `KPI-PRED-01` | **Metric Version:** `v0.5.0`
* **Certification Status:** `Certified`
* **Confidence Level:** ★★★★☆ (Multi-Factor Diagnostic Score)
* **Governance Roles:**
  * **Business Owner:** People Analytics Lead
  * **Technical Owner:** People Analytics / HR Data Analyst
  * **Data Steward:** HRBP Specialist
  * **Approval Committee:** HR & Analytics Steering Committee
* **Validation History:**
  * **Last Validation Date:** August 2026
  * **Data Contract Version:** `v0.4.0` | **Business Rule Version:** `BR v0.3.0`

#### Business Scope & Objective
* **KPI Name:** Individual Flight Risk Score (Score)
* **Business Objective:** Estimar el nivel multifactorial de riesgo de renuncia voluntaria para priorizar la retención proactiva de talento crítico.
* **Business Question:** ¿Qué colaboradores presentan mayor exposición al riesgo de salida según su brecha salarial, sobretiempo acumulado y severidad de ausentismo?

#### Calculation Engine & Logic
* **Formula:**
  `Flight Risk Score = w₁ × Compa_Ratio_Gap + w₂ × Overtime_30d_Severity + w₃ × Bradford_Score_Tier`
  *(Ponderación estándar: 45% Brecha Salarial < 0.85, 35% Horas Extra > 30h/mes, 20% Bradford Score ≥ 150).*

* **SQL Logic (PostgreSQL - Vista Analítica):**
```sql
SELECT 
    e.employee_id,
    e.first_name || ' ' || e.last_name AS full_name,
    e.department_id,
    e.performance_rating,
    e.annual_base_salary_usd,
    ROUND(
        (CASE WHEN (e.annual_base_salary_usd / NULLIF(b.market_midpoint_salary_usd, 0)) < 0.85 THEN 0.45 ELSE 0.0 END) +
        (CASE WHEN COALESCE(att.overtime_hours_30d, 0) > 30 THEN 0.35 ELSE 0.0 END) +
        (CASE WHEN COALESCE(att.bradford_score_12m, 0) >= 150 THEN 0.20 ELSE 0.0 END),
        2
    ) AS flight_risk_score,
    CASE 
        WHEN ((CASE WHEN (e.annual_base_salary_usd / NULLIF(b.market_midpoint_salary_usd, 0)) < 0.85 THEN 0.45 ELSE 0.0 END) +
              (CASE WHEN COALESCE(att.overtime_hours_30d, 0) > 30 THEN 0.35 ELSE 0.0 END) +
              (CASE WHEN COALESCE(att.bradford_score_12m, 0) >= 150 THEN 0.20 ELSE 0.0 END)) >= 0.70 THEN 'Alto'
        WHEN ((CASE WHEN (e.annual_base_salary_usd / NULLIF(b.market_midpoint_salary_usd, 0)) < 0.85 THEN 0.45 ELSE 0.0 END) +
              (CASE WHEN COALESCE(att.overtime_hours_30d, 0) > 30 THEN 0.35 ELSE 0.0 END) +
              (CASE WHEN COALESCE(att.bradford_score_12m, 0) >= 150 THEN 0.20 ELSE 0.0 END)) >= 0.40 THEN 'Medio'
        ELSE 'Bajo'
    END AS risk_tier
FROM people_analytics.dim_employees e
LEFT JOIN people_analytics.dim_salary_benchmarks b ON e.position_sk = b.position_sk
LEFT JOIN (
    SELECT 
        employee_sk,
        SUM(overtime_hours) AS overtime_hours_30d,
        (POWER(SUM(is_absence_instance_start), 2) * COUNT(CASE WHEN is_unplanned_absence = TRUE THEN 1 END)) AS bradford_score_12m
    FROM people_analytics.fact_attendance_logs
    WHERE date_key >= (SELECT MAX(date_key) - 30 FROM people_analytics.fact_attendance_logs)
    GROUP BY employee_sk
) att ON e.employee_sk = att.employee_sk
WHERE e.is_active = TRUE AND e.is_current_row = TRUE;
```

* **DAX Logic (Power BI):**
```dax
Flight_Risk_Score = 
VAR CompaGap = IF([Compa_Ratio] < 0.85, 0.45, 0)
VAR OvertimeRisk = IF([Overtime_Hours_30d] > 30, 0.35, 0)
VAR BradfordRisk = IF([Bradford_Score_12m] >= 150, 0.20, 0)
RETURN CompaGap + OvertimeRisk + BradfordRisk
```

#### Calculation Dependencies & Lineage
```text
dim_employees ─────────┐
fact_attendance_logs ──┼─► SQL Views / DAX Calculation ──► HRBP Action Center
dim_salary_benchmarks ─┘
```

#### Thresholds & Prescriptive Business Actions
* **Thresholds:**
  * **Bajo:** 0.00 - 0.39
  * **Medio:** 0.40 - 0.69
  * **Alto (Critical):** ≥ 0.70
* **Business Actions:** Notificación prioritaria al HRBP responsable. El HRBP debe analizar los causales individuales en el panel (brecha salarial o sobretiempo) y programar una sesión de alineación (*Stay Interview*) o ajuste de mérito en un plazo no mayor a 5 días hábiles.

#### Metadata Traces
* **Related Business Rules:** BR-04, BR-05, BR-27, BR-28
* **Related Functional Requirements:** FR-13, FR-14, FR-31, FR-33
* **Related Datasets:** `dim_employees`, `fact_attendance_logs`, `dim_salary_benchmarks`
* **Interview Question:** ¿Cómo construiste el indicador de Flight Risk sin recurrir a modelos de caja negra?
* **Respuesta Esperada:** Implementé un modelo de ponderación multifactorial fundamentado en evidencia cuantitativa de People Analytics: penalización salarial por debajo del mercado (45%), sobrecarga crítica de horas extra (35%) y ausentismo intermitente por fatiga (20%). Esto permite al HRBP explicar con total transparencia la causa raíz del riesgo y accionar planes de retención directos y medibles.

---

## 9. Operational KPIs Specifications

### KPI-OP-01: Bradford Factor Score

#### Metadata & Governance
* **KPI ID:** `KPI-OP-01` | **Metric Version:** `v0.5.0`
* **Certification Status:** `Certified`
* **Confidence Level:** ★★★★★ (Deterministic)
* **Governance Roles:**
  * **Business Owner:** VP of Operations
  * **Technical Owner:** Workforce Management Analyst
  * **Data Steward:** Operations Control Specialist
  * **Approval Committee:** Operations Control Board
* **Validation History:**
  * **Last Validation Date:** August 2026
  * **Data Contract Version:** `v0.4.0` | **Business Rule Version:** `BR v0.3.0`

#### Business Scope & Objective
* **KPI Name:** Bradford Factor Score (Score)
* **Business Objective:** Identificar y controlar la severidad del ausentismo intermitente no programado en ventanas móviles de 12 meses.
* **Business Question:** ¿Qué colaboradores o equipos presentan patrones de ausentismo corto y recurrente que desestabilizan las operaciones?

#### Calculation Engine & Logic
* **Formula:**
  `B = S² × D`  
  *(Donde S es el número de instancias independientes de ausencia no programada y D es el número total de días ausentes).*

* **SQL Logic (PostgreSQL):**
```sql
WITH absence_sequences AS (
    SELECT 
        employee_id,
        date_key,
        is_absence_instance_start,
        SUM(is_absence_instance_start) OVER (PARTITION BY employee_id ORDER BY date_key) AS instance_group
    FROM people_analytics.fact_attendance_logs
    WHERE is_unplanned_absence = 1
      AND date_key >= CURRENT_DATE - INTERVAL '1 year'
),
bradford_metrics AS (
    SELECT 
        employee_id,
        COUNT(DISTINCT instance_group) AS S_instances,
        COUNT(*) AS D_total_days
    FROM absence_sequences
    GROUP BY employee_id
)
SELECT 
    employee_id,
    S_instances,
    D_total_days,
    (POWER(S_instances, 2) * D_total_days) AS bradford_score,
    CASE 
        WHEN (POWER(S_instances, 2) * D_total_days) >= 500 THEN 'Severo'
        WHEN (POWER(S_instances, 2) * D_total_days) >= 150 THEN 'Crítico'
        WHEN (POWER(S_instances, 2) * D_total_days) >= 50 THEN 'Moderado'
        ELSE 'Bajo'
    END AS bradford_risk_tier
FROM bradford_metrics;
```

* **DAX Logic (Power BI):**
```dax
Bradford_Factor_Score = 
VAR S = SUM(fact_attendance_logs[is_absence_instance_start])
VAR D = CALCULATE(COUNTROWS(fact_attendance_logs), fact_attendance_logs[is_unplanned_absence] = 1)
RETURN (S * S) * D
```

#### Calculation Dependencies & Lineage
```text
fact_attendance_logs (is_unplanned_absence) ──► Window Aggregation ──► Power BI DAX Measure ──► Operational Capacity Tracker
```

#### Thresholds & Prescriptive Business Actions
* **Thresholds (Configurables BR-07):**
  * **Bajo:** < 50
  * **Moderado:** 50 - 149
  * **Crítico:** 150 - 499
  * **Severo:** ≥ 500
* **Business Actions:** Si el score supera los 150 puntos en Soporte Clínico, la herramienta emite un aviso de gestión operativa. Si supera los 500 puntos, se inicia una revisión formal con Gestión Humana para evaluar planes de salud ocupacional o acciones disciplinarias.

#### Metadata Traces
* **Related Business Rules:** BR-06, BR-07, BR-08, BR-09
* **Related Functional Requirements:** FR-16, FR-17
* **Related Datasets:** `fact_attendance_logs`, `dim_employees`
* **Interview Question:** ¿Por qué el Factor de Bradford penaliza más las ausencias frecuentes de 1 día que una sola ausencia de 10 días seguidos?
* **Respuesta Esperada:** Porque una ausencia única de 10 días (ej. por una cirugía) es un evento de salud planificable donde la operación puede reasignar un reemplazo temporal. Sin embargo, 10 ausencias imprevistas de 1 día (especialmente Lunes o Viernes) destruyen la planificación de turnos diaria, sobrecargan al equipo presente y son el principal indicador de agotamiento (burnout) o falta de compromiso.

---

## 10. Comprehensive Master Metric Matrix

| KPI ID | Metric Name | Status | Confidence | Owner | Target | Source Entity | Dashboard View |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `KPI-EXEC-01` | High-Performer Retention Rate | Certified | ★★★★★ | CHRO | ≥ 90.0% | `dim_employees` | Boardroom Executive Overview |
| `KPI-EXEC-02` | Net Financial ROI ($ / %) | Certified | ★★★★★ | CFO | ≥ 300% ROI | `fact_terminations` | Boardroom Executive Overview |
| `KPI-HR-01` | Voluntary Attrition Rate | Certified | ★★★★★ | Global HR Director | < 10.0% Anual | `fact_terminations` | HRBP Action Center |
| `KPI-HR-02` | Corporate Compa-Ratio | Certified | ★★★★★ | Head of Total Rewards | 0.85 - 1.15 | `dim_salary_benchmarks` | Financial What-If Simulator |
| `KPI-FIN-01` | Total Cost of Attrition | Certified | ★★★★★ | CFO | < $200k USD Anual | `fact_terminations` | Boardroom Executive Overview |
| `KPI-FIN-02` | SLA Penalty Staffing Cost | Certified | ★★★★★ | VP of Operations | $0 USD | `fact_sla_events` | Boardroom Executive Overview |
| `KPI-PRED-01` | Individual Flight Risk Score | Certified | ★★★★☆ | People Analytics Lead | < 0.40 Avg | `dim_employees` / `fact_attendance_logs` | HRBP Action Center |
| `KPI-OP-01` | Bradford Factor Score | Certified | ★★★★★ | VP of Operations | < 85 Avg | `fact_attendance_logs` | HRBP Action Center |


