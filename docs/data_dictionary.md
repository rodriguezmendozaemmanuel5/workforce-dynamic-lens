# DATA DICTIONARY & ENTERPRISE DATA CONTRACT
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & WORKFORCE DYNAMICS SOLUTION

**Document Version:** v0.4.0 (Finalized Enterprise Data Contract Baseline)  
**Target Audience:** Executive Committee, People Analytics Leaders, HR Data Analysts, BI Developers, Governance Lead  
**Document Owner:** Emmanuel Rodríguez Mendoza  
**Professional Role:** People Analytics / HR Data Analyst  
**Project:** Workforce Dynamic Lens  
**Date:** 2026-08-04  
**Status:** Approved Data Contract Baseline  

---

## 1. Document Purpose & Global Metadata

El propósito de este **Data Dictionary & Enterprise Data Contract** es establecer el acuerdo técnico y de negocio vinculante que gobierna la estructura, el significado, el ciclo de vida, la calidad y las políticas de seguridad de los datos para la plataforma **Workforce Dynamic Lens (v0.4.0)** en MedTech Global Solutions.

Este documento actúa como un **Data Contract de clase empresarial** entre los sistemas fuente de Recursos Humanos, Operaciones y Finanzas, el pipeline de datos, las consultas analíticas en SQL y la capa de visualización ejecutiva en Power BI. Garantiza trazabilidad auditable hacia los 42 Requerimientos Funcionales (FR), 32 Reglas de Negocio (BR) y 31 Preguntas de Negocio definidos en el BRD v0.3.0.

### Global System Metadata
```text
┌──────────────────────────────────────────────────────────────────────────┐
│ GLOBAL SYSTEM METADATA                                                   │
├──────────────────────────────┬───────────────────────────────────────────┤
│ Target Database Engine       │ PostgreSQL 16+ (ANSI SQL Standard)        │
│ Database Schema Name         │ people_analytics                          │
│ Schema Version               │ v0.4.0                                    │
│ Timezone Standard            │ UTC (Coordinated Universal Time)          │
│ Primary Code Repository      │ github.com/rodriguezmendozaemmanuel5/workforce-dynamic-lens │
│ Primary Language Standard    │ Spanish (Executive Body) / English (Code) │
│ Governance Framework         │ Enterprise Data Governance (GDPR / LATAM) │
└──────────────────────────────┴───────────────────────────────────────────┘
```

---

## 2. Scope

El alcance de este contrato de datos abarca la totalidad de las 7 entidades relacionales analíticas diseñadas para modelar el comportamiento operativo y financiero de **4,500 colaboradores** distribuidos en LATAM y Europa:

* **Tablas de Dimensión (3):** `dim_employees`, `dim_departments`, `dim_positions`.
* **Tablas de Referencia / Marcadores (1):** `dim_salary_benchmarks`.
* **Tablas de Hechos / Transaccionales (3):** `fact_attendance_logs`, `fact_terminations`, `fact_sla_events`.

---

## 3. Data Governance Principles & Ownership Matrix

### 3.1 Governance Principles

1. **Single Source of Truth (SSOT):** Cada atributo de capital humano tiene un único propietario de negocio (*Business Owner*) y un único sistema de origen autorizado.
2. **Data Minimization & Privacy by Design:** Solo se procesan los datos personales estrictamente necesarios para cumplir con los objetivos analíticos aprobados.
3. **Data Quality at Ingress:** La calidad de los datos se valida en la capa de ingesta (*Ingress Layer*). Los registros que violen las reglas de calidad críticas se rechazan o aíslan en tablas de cuarentena.
4. **Immutability of Historical Facts:** Los eventos registrados en las tablas de hechos (`fact_*`) son inmutables. Las correcciones se realizan mediante eventos compensatorios.
5. **Decoupled Architecture:** La capa analítica almacena datos primarios estandarizados; los indicadores derivados dinámicos (*Compa-Ratio*, *Bradford Factor*) se calculan mediante transformaciones deterministas explícitas.

### 3.2 Data Ownership Matrix
```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ENTERPRISE DATA OWNERSHIP MATRIX                                                                                       │
├──────────────────────────┬──────────────────────────────┬─────────────────────────────┬────────────────────────────────┤
│ Data Domain              │ Business Owner               │ Technical Owner             │ Data Steward                   │
├──────────────────────────┼──────────────────────────────┼─────────────────────────────┼────────────────────────────────┤
│ Employee Master Data     │ Global HR Director           │ People Analytics / Data Team│ HRIS Operations Specialist     │
│ Org & Position Catalog   │ Compensation & HR Strategy   │ People Analytics / Data Team│ Job Architecture Specialist    │
│ Salary Benchmarks        │ Head of Total Rewards        │ People Analytics / Data Team│ Compensation Analyst           │
│ Attendance & Time Logs   │ VP of Operations             │ People Analytics / Data Team│ Workforce Management Analyst   │
│ Exit & Terminations      │ Global HR Director           │ People Analytics / Data Team│ People Operations Specialist   │
│ SLA & Operational Cost   │ VP of Operations             │ People Analytics / Data Team│ Operations Service Manager     │
└──────────────────────────┴──────────────────────────────┴─────────────────────────────┴────────────────────────────────┘
```

---

## 4. Business Glossary

Para evitar discrepancias conceptuales entre las áreas tecnológicas y ejecutivas, los principales conceptos del dominio de **People Analytics** se definen de la siguiente manera:

* **Compa-Ratio (CR):** Indicador de competitividad salarial individual que evalúa la posición del salario base de un colaborador respecto al punto medio de mercado (*Midpoint*):
  `Compa-Ratio = Salario Base Anual (USD) / Punto Medio de Mercado (USD)`
* **Factor de Bradford (B):** Indicador ponderado utilizado para medir la severidad del ausentismo intermitente de corta duración en un periodo de 12 meses:
  `B = S² × D`
*Donde S es el número de instancias de ausencia independientes y D es el total de días ausentes.*
* **High-Performer (Talento Clave):** Colaborador activo con una evaluación de desempeño oficial igual o superior a 4.0 en la escala estandarizada de 1.0 a 5.0.
* **Flight Risk Score:** Puntuación probabilística (0.00 a 1.00) generada por modelos analíticos que indica la probabilidad de renuncia voluntaria de un colaborador en un horizonte de 90 días.
* **Regrettable Attrition (Rotación No Deseada):** Desvinculación voluntaria de un colaborador calificado como *High-Performer* o que ocupa una posición crítica para la empresa.
* **Time-to-Fill:** Días continuos transcurridos desde la aprobación formal de una vacante hasta la aceptación formal de la oferta de empleo por el candidato.
* **Time-to-Full Productivity:** Días transcurridos desde la fecha de ingreso oficial del colaborador hasta alcanzar el 100% de la cuota de desempeño requerida para su puesto.
* **Fully-Loaded Salary Cost:** Costo laboral anual total que incluye el salario base abonado más un **30% adicional** correspondiente a cargas prestacionales obligatorias y beneficios.

---

## 5. Naming Conventions & Data Standards

### Naming Conventions

* **Database Entities & Columns:** Estricto formato `snake_case` en minúsculas (ej. `employee_id`, `annual_base_salary_usd`).
* **Primary Keys:** Identificador `snake_case` con prefijo de la entidad (ej. `employee_id` en `dim_employees`).
* **Foreign Keys:** Mismo nombre exacto que la clave primaria de la dimensión mapeada.
* **Monetary Values:** Unidad explícita en la denominación (ej. `_usd` o `_orig`) y almacenados convertidos a USD.
* **Flags / Booleans:** Prefijos descriptivos `is_` o `has_` con valores binarios `1` (Verdadero) o `0` (Falso).
* **Date & Time Attributes:** Sufijos explícitos `_date` para fechas YYYY-MM-DD y `_timestamp` para marcas UTC.

### Data Standards

* **Encoding:** UTF-8 sin BOM para soporte multilenguaje.
* **Currency Standard:** Dólar Estadounidense (USD) como moneda contable consolidada primariamente, manteniendo `salary_currency_orig` para auditoría local.
* **Date Standard:** ISO 8601 (`YYYY-MM-DD`).
* **Timestamp Standard:** ISO 8601 UTC (`YYYY-MM-DD HH:MM:SS`).
* **Null Value Representation:** Representados estrictamente como `NULL` en base de datos; prohibido el uso de cadenas vacías `""` o números mágicos (`-999`, `9999-12-31`).

---

## 6. Entity Overview
```text
                      ┌────────────────────────┐
                      │    dim_departments     │
                      └───────────┬────────────┘
                                  │ 1:N
                                  ▼
┌───────────────────────┐   ┌───────────────────┐   ┌────────────────────────┐
│     dim_positions     │──►│   dim_employees   │◄──│ dim_salary_benchmarks  │
└───────────────────────┘1:N└─────────┬─────────┘1:N└────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │ 1:N                       │ 1:N                       │ 1:N
          ▼                           ▼                           ▼
┌───────────────────────┐   ┌───────────────────┐   ┌────────────────────────┐
│ fact_attendance_logs  │   │ fact_terminations │   │    fact_sla_events     │
└───────────────────────┘   └───────────────────┘   └────────────────────────┘
```

| Entity Name | Type | Grain | Primary Key | Business Owner | Refresh |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dim_employees` | Dimension | 1 fila por colaborador activo o histórico | `employee_id` | Human Resources | Daily |
| `dim_departments` | Dimension | 1 fila por área / departamento funcional | `department_id` | Corporate Operations | Monthly |
| `dim_positions` | Dimension | 1 fila por catálogo de puesto / rol | `position_id` | Compensation & Talent | Monthly |
| `dim_salary_benchmarks`| Benchmark | 1 fila por puesto, país y año de estudio | `benchmark_id` | Compensation | Bi-annually |
| `fact_attendance_logs` | Fact | 1 fila por colaborador y día calendario | `attendance_id` | HR Operations | Daily |
| `fact_terminations` | Fact | 1 fila por evento de desvinculación | `termination_id` | Human Resources | Daily |
| `fact_sla_events` | Fact | 1 fila por evento de penalización/breach SLA| `sla_event_id` | Clinical Operations | Daily |

---

## 7. Entity Documentation

### 7.1 Entity: `dim_employees`

#### Technical Metadata
* **Business Owner:** Global Human Resources
* **Technical Owner:** People Analytics / HR Data Analyst
* **Data Steward:** HRIS Operations Specialist
* **Primary Key:** `employee_id`
* **Grain:** Un registro por cada colaborador activo o histórico ingresado a la compañía.
* **Refresh Frequency:** Diario (Nightly ETL)
* **Source System:** HRIS Core (Workday / BambooHR)
* **Estimated Rows:** 4,500 activos + 1,200 históricos (~5,700 registros total)
* **Retention Policy:** 7 años post-desvinculación
* **Contains PII:** Yes
* **GDPR Classification:** Confidential / Restricted

#### Column Specifications

| Campo | Tipo | PK/FK | Nullable | Descripción | Unidad | Dominio | Ejemplo | Regla de Validación | PII | Sensibilidad | Origen | BR Mapeadas | FR Mapeadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `employee_id` | `VARCHAR(10)` | PK | No | Identificador único global del empleado | Text | Pattern `EMP\d{5}` | `EMP01420` | Único, No Nulo, Inmutable | No | Internal | HRIS | BR-01 | FR-01, FR-06 |
| `first_name` | `VARCHAR(50)` | - | No | Primer nombre del colaborador | Text | Nombres válidos UTF-8 | `Carlos` | No Nulo, Max 50 chars | Sí | Confidential | HRIS | - | FR-01, FR-41 |
| `last_name` | `VARCHAR(50)` | - | No | Apellidos del colaborador | Text | Apellidos válidos UTF-8 | `Mendoza` | No Nulo, Max 50 chars | Sí | Confidential | HRIS | - | FR-01, FR-41 |
| `work_email` | `VARCHAR(100)`| - | No | Correo electrónico corporativo | Email | Format `.*@medtech\.com` | `cmendoza@medtech.com` | Único, Válido sintaxis email | Sí | Confidential | HRIS | - | FR-01, FR-41 |
| `gender` | `VARCHAR(20)` | - | No | Género autoreportado del colaborador | Code | `Femenino`, `Masculino`, `No Binario` | `Masculino` | En catálogo de género | Sí | Confidential | HRIS | BR-23 | FR-01, FR-23, FR-24 |
| `birth_date` | `DATE` | - | No | Fecha de nacimiento | YYYY-MM-DD | `1950-01-01` a `2008-01-01` | `1992-05-14` | Edad entre 18 y 75 años | Sí | Restricted | HRIS | - | FR-01 |
| `hire_date` | `DATE` | - | No | Fecha oficial de ingreso a la empresa | YYYY-MM-DD | `2015-01-01` a `Current_Date` | `2021-03-15` | ≤ Fecha Actual, ≥ Nacer + 18 años | No | Internal | HRIS | BR-01, BR-20 | FR-01, FR-12 |
| `department_id` | `VARCHAR(10)` | FK | No | Clave foránea al departamento asignado | Text | `dim_departments.department_id` | `DEP_RD` | Debe existir en `dim_departments` | No | Internal | HRIS | - | FR-01, FR-10 |
| `position_id` | `VARCHAR(10)` | FK | No | Clave foránea al puesto o rol asignado | Text | `dim_positions.position_id` | `POS_ENG_SR` | Debe existir en `dim_positions` | No | Internal | HRIS | BR-03 | FR-01, FR-11 |
| `country_code` | `VARCHAR(3)` | - | No | Código ISO Alpha-3 del país de contrato | Code | `COL`, `MEX`, `ESP`, `DEU` | `COL` | En catálogo ISO-3 | No | Internal | HRIS | BR-12 | FR-01, FR-08 |
| `work_location_type`| `VARCHAR(20)`| - | No | Modalidad de trabajo contractual | Code | `Presencial`, `Híbrido`, `Remoto` | `Remoto` | En valores autorizados | No | Internal | HRIS | - | FR-01 |
| `base_salary_orig` | `DECIMAL(12,2)`| - | No | Salario base mensual en moneda local | Currency | > 0.00 | `12500000.00` | Valor numérico positivo | Sí | Restricted | Payroll | BR-11 | FR-01, FR-08 |
| `salary_currency_orig`| `VARCHAR(3)`| - | No | Moneda local del contrato (ISO 4217) | Code | `COP`, `MXN`, `EUR`, `USD` | `COP` | En catálogo ISO-4217 | No | Internal | Payroll | BR-12 | FR-01, FR-08 |
| `annual_base_salary_usd`|`DECIMAL(12,2)`| - | No | Salario base fijado anualizado en USD | USD | > 0.00 | `38500.00` | `= (base_salary_orig * 12) * fx_rate` | Sí | Restricted | Derived/Calculated| BR-10, BR-11 | FR-08, FR-21 |
| `fully_loaded_cost_usd`|`DECIMAL(12,2)`| - | No | Costo laboral anual total cargado (30%) | USD | > 0.00 | `50050.00` | `= annual_base_salary_usd * 1.30` | Sí | Restricted | Derived/Calculated| BR-16, BR-17 | FR-26, FR-28 |
| `performance_rating`| `DECIMAL(3,2)`| - | Yes | Calificación de desempeño (Escala 1-5)| Score | `1.00` a `5.00` | `4.20` | Null si nuevo ingreso (< 6 meses) | Sí | Confidential | HRIS Performance| BR-03, BR-24, BR-31| FR-01, FR-11, FR-22 |
| `potential_rating` | `VARCHAR(10)` | - | Yes | Evaluación 9-Box de potencial | Code | `Bajo`, `Medio`, `Alto` | `Alto` | En catálogo 9-Box | Sí | Confidential | HRIS Performance| - | FR-01 |
| `is_active` | `SMALLINT` | - | No | Bandera de estado activo en plantilla | Binary | `0` (Inactivo), `1` (Activo) | `1` | `0` si existe fecha de egreso | No | Internal | HRIS | BR-01 | FR-01, FR-10 |

---

### 7.2 Entity: `dim_departments`

#### Technical Metadata
* **Business Owner:** Corporate Operations & VP of Operations
* **Technical Owner:** People Analytics / HR Data Analyst
* **Data Steward:** Job Architecture Specialist
* **Primary Key:** `department_id`
* **Grain:** Un registro por cada departamento o unidad organizativa funcional.
* **Refresh Frequency:** Mensual
* **Source System:** HRIS Organizational Structure
* **Estimated Rows:** 15 - 25 departamentos
* **Retention Policy:** Permanente
* **Contains PII:** No
* **GDPR Classification:** Internal

#### Column Specifications

| Campo | Tipo | PK/FK | Nullable | Descripción | Unidad | Dominio | Ejemplo | Regla de Validación | PII | Sensibilidad | Origen | BR Mapeadas | FR Mapeadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `department_id` | `VARCHAR(10)` | PK | No | Identificador único del departamento | Text | Pattern `DEP_[A-Z0-9]+` | `DEP_RD` | Único, No Nulo | No | Internal | HRIS Org | - | FR-01 |
| `department_name` | `VARCHAR(100)`| - | No | Nombre oficial del área funcional | Text | Nombres de áreas aprobados | `Investigación y Desarrollo`| No Nulo | No | Internal | HRIS Org | - | FR-01, FR-10 |
| `cost_center_code`| `VARCHAR(20)` | - | No | Código contable de centro de costos | Text | Pattern `CC-\d{4}` | `CC-4010` | Formato contable válido | No | Internal | Finance ERP | - | FR-01 |
| `vp_responsible` | `VARCHAR(100)`| - | No | Nombre del VP o Director del área | Text | Nombre de ejecutivo | `Johan Lindqvist` | No Nulo | No | Internal | HRIS Org | - | FR-01 |
| `region` | `VARCHAR(20)` | - | No | Región geográfica principal de operación| Code | `LATAM`, `Europa`, `Global` | `LATAM` | En catálogo de regiones | No | Internal | HRIS Org | - | FR-01, FR-10 |
| `budget_annual_usd`|`DECIMAL(14,2)`| - | No | Presupuesto operativo anual en USD | USD | > 0.00 | `2500000.00` | Valor numérico positivo | No | Confidential | Finance ERP | - | FR-01 |
| `target_headcount` | `INT` | - | No | Capacidad de plantilla aprobada (Dotación)| Count | > 0 | `120` | Entero positivo | No | Internal | Workforce Plan| BR-32 | FR-01, FR-27 |
| `strategic_level` | `VARCHAR(20)` | - | No | Nivel de criticidad estratégica del área | Code | `Core Revenue`, `Operation Critical`, `Support` | `Core Revenue` | En catálogo estratégico | No | Internal | HR Strategy | BR-16, BR-25 | FR-01, FR-11 |

---

### 7.3 Entity: `dim_positions`

#### Technical Metadata
* **Business Owner:** Compensation & HR Strategy
* **Technical Owner:** People Analytics / HR Data Analyst
* **Data Steward:** Job Architecture Specialist
* **Primary Key:** `position_id`
* **Grain:** Un registro por cada rol o título de puesto formal en el catálogo corporativo.
* **Refresh Frequency:** Mensual
* **Source System:** Job Architecture Catalog
* **Estimated Rows:** 80 - 150 posiciones
* **Retention Policy:** Permanente
* **Contains PII:** No
* **GDPR Classification:** Internal

#### Column Specifications

| Campo | Tipo | PK/FK | Nullable | Descripción | Unidad | Dominio | Ejemplo | Regla de Validación | PII | Sensibilidad | Origen | BR Mapeadas | FR Mapeadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `position_id` | `VARCHAR(10)` | PK | No | Identificador único del puesto | Text | Pattern `POS_[A-Z0-9]+` | `POS_ENG_SR` | Único, No Nulo | No | Internal | Job Architecture| - | FR-01 |
| `job_title` | `VARCHAR(100)`| - | No | Título oficial de la posición | Text | Catálogo de roles | `Senior Software Engineer`| No Nulo | No | Internal | Job Architecture| - | FR-01, FR-28 |
| `job_family` | `VARCHAR(50)` | - | No | Familia profesional de pertenencia | Code | `Engineering`, `Clinical Support`, `Sales`, `HR` | `Engineering` | En catálogo de familias | No | Internal | Job Architecture| - | FR-01 |
| `job_grade` | `VARCHAR(10)` | - | No | Banda o grado jerárquico corporativo | Code | `G1` a `G10` | `G7` | Patrón G + número | No | Internal | Compensation | BR-10 | FR-01, FR-21 |
| `career_level` | `VARCHAR(20)` | - | No | Nivel de madurez profesional | Code | `Junior`, `SemiSenior`, `Senior`, `Lead`, `Director`| `Senior` | En catálogo de niveles | No | Internal | Job Architecture| BR-16, BR-20 | FR-01, FR-12 |
| `is_critical_position`|`SMALLINT`| - | No | Bandera de puesto clave o difícil reemplazo| Binary| `0` (Normal), `1` (Crítico) | `1` | Obligatorio 0 o 1 | No | Internal | Talent Strategy | BR-03, BR-25 | FR-01, FR-11 |
| `is_remote_eligible` |`SMALLINT`| - | No | Elegibilidad contractual para trabajo remoto| Binary| `0` (No), `1` (Sí) | `1` | Obligatorio 0 o 1 | No | Internal | HR Policy | - | FR-01 |
| `market_scarcity_index`|`DECIMAL(3,2)`| - | No | Índice de escasez de talento en mercado | Index | `1.00` (Bajo) a `3.00` (Extremo) | `2.40` | Rango numérico entre 1.0 y 3.0| No | Internal | External Intelligence| BR-16 | FR-03, FR-28 |

---

### 7.4 Entity: `dim_salary_benchmarks`

#### Technical Metadata
* **Business Owner:** Head of Total Rewards
* **Technical Owner:** People Analytics / HR Data Analyst
* **Data Steward:** Compensation Analyst
* **Primary Key:** `benchmark_id`
* **Grain:** Un registro por puesto, país y versión de estudio de mercado salarial.
* **Refresh Frequency:** Semestral / Anual
* **Source System:** External Labor Market Intelligence Providers
* **Estimated Rows:** 300 - 500 registros
* **Retention Policy:** 5 años
* **Contains PII:** No
* **GDPR Classification:** Internal

#### Column Specifications

| Campo | Tipo | PK/FK | Nullable | Descripción | Unidad | Dominio | Ejemplo | Regla de Validación | PII | Sensibilidad | Origen | BR Mapeadas | FR Mapeadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `benchmark_id` | `VARCHAR(15)` | PK | No | Identificador del registro de mercado | Text | Pattern `BMK_[A-Z0-9_]+` | `BMK_ENG_SR_COL_26`| Único, No Nulo | No | Internal | Compensation | - | FR-03 |
| `position_id` | `VARCHAR(10)` | FK | No | Clave foránea al puesto de referencia | Text | `dim_positions.position_id` | `POS_ENG_SR` | Debe existir en `dim_positions` | No | Internal | Compensation | - | FR-03, FR-21 |
| `country_code` | `VARCHAR(3)` | - | No | Código ISO-3 del país del mercado | Code | `COL`, `MEX`, `ESP`, `DEU` | `COL` | En catálogo ISO-3 | No | Internal | External Intelligence| BR-12 | FR-03, FR-08 |
| `market_min_salary_usd`|`DECIMAL(12,2)`| - | No | Percentil 25 (P25) de mercado en USD | USD | > 0.00 | `30000.00` | `< market_midpoint` | No | Internal | External Intelligence| BR-10, BR-13 | FR-03, FR-21 |
| `market_midpoint_salary_usd`|`DECIMAL(12,2)`| - | No | Percentil 50 (P50 / Midpoint) en USD | USD | > 0.00 | `40000.00` | `> P25 y < P75` | No | Internal | External Intelligence| BR-10, BR-13 | FR-03, FR-21 |
| `market_max_salary_usd`|`DECIMAL(12,2)`| - | No | Percentil 75 (P75) de mercado en USD | USD | > 0.00 | `52000.00` | `> market_midpoint` | No | Internal | External Intelligence| BR-10, BR-13 | FR-03, FR-21 |
| `survey_provider` | `VARCHAR(50)` | - | No | Denominación del proveedor de estudio | Text | `External labor market intelligence providers`| `Market Intelligence Provider A`| No Nulo | No | Internal | External Intelligence| BR-13 | FR-03 |
| `effective_year` | `INT` | - | No | Año fiscal de vigencia del marcador | Year | `2024` a `2030` | `2026` | Año válido | No | Internal | External Intelligence| BR-13 | FR-03 |

---

### 7.5 Entity: `fact_attendance_logs`

#### Technical Metadata
* **Business Owner:** VP of Operations
* **Technical Owner:** People Analytics / HR Data Analyst
* **Data Steward:** Workforce Management Analyst
* **Primary Key:** `attendance_id`
* **Grain:** Un registro por cada colaborador y cada día calendario de registro operativo.
* **Refresh Frequency:** Diario (Nightly ETL Batch)
* **Source System:** Time & Attendance System / Clock-In Logs
* **Estimated Rows:** ~1.6 Millones de registros por año (4,500 emp × 365 días)
* **Retention Policy:** 3 años primario; 7 años archivado
* **Contains PII:** No (Utiliza `employee_id` como clave pseudo-anonimizada)
* **GDPR Classification:** Confidential

#### Column Specifications

| Campo | Tipo | PK/FK | Nullable | Descripción | Unidad | Dominio | Ejemplo | Regla de Validación | PII | Sensibilidad | Origen | BR Mapeadas | FR Mapeadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `attendance_id` | `VARCHAR(20)` | PK | No | Identificador único de la transacción | Text | Pattern `ATT_\d{12}` | `ATT_202608040001` | Único, No Nulo | No | Internal | Time Tracker | - | FR-02 |
| `employee_id` | `VARCHAR(10)` | FK | No | Clave foránea del colaborador | Text | `dim_employees.employee_id` | `EMP01420` | Debe existir en `dim_employees` | No | Confidential | Time Tracker | BR-06, BR-08 | FR-02, FR-16 |
| `date_key` | `DATE` | - | No | Fecha del registro de asistencia | YYYY-MM-DD | `2024-01-01` a `Current_Date` | `2026-08-04` | Fecha ISO válida | No | Internal | Time Tracker | BR-08, BR-21 | FR-02, FR-20 |
| `shift_type` | `VARCHAR(20)` | - | No | Turno operativo programado | Code | `Mañana`, `Tarde`, `Noche`, `Central` | `Mañana` | En catálogo de turnos | No | Internal | Workforce Plan| BR-14, BR-32 | FR-02, FR-19 |
| `clock_in_time` | `TIMESTAMP` | - | Yes | Marca de tiempo exacta de ingreso UTC | UTC | Timestamp ISO | `2026-08-04 07:02:15` | Null si hubo ausencia | No | Confidential | Time Tracker | - | FR-02 |
| `clock_out_time` | `TIMESTAMP` | - | Yes | Marca de tiempo exacta de salida UTC | UTC | Timestamp ISO | `2026-08-04 17:30:00` | > clock_in_time | No | Confidential | Time Tracker | - | FR-02 |
| `planned_hours` | `DECIMAL(4,2)`| - | No | Horas laborales programadas según contrato| Hours | `0.00` a `12.00` | `8.00` | ≥ 0.00 | No | Internal | Workforce Plan| BR-08 | FR-02, FR-19 |
| `actual_hours_worked`|`DECIMAL(4,2)`| - | No | Horas efectivas trabajadas según marcas | Hours | `0.00` a `16.00` | `8.50` | ≥ 0.00 | No | Internal | Time Tracker | - | FR-02, FR-19 |
| `overtime_hours` | `DECIMAL(4,2)`| - | No | Horas extra autorizadas y laboradas | Hours | `0.00` a `8.00` | `2.50` | `= MAX(0, actual - planned)`| No | Internal | Derived/Calculated| BR-21 | FR-02, FR-18 |
| `absence_type` | `VARCHAR(30)` | - | Yes | Clasificación del evento de ausencia | Code | `Incapacidad Medica`, `Vacaciones`, `Injustificada`, `Licencia`| `Incapacidad Medica`| Null si asistió a trabajar | No | Internal | HR Operations | BR-09 | FR-02, FR-17 |
| `is_unplanned_absence`|`SMALLINT`| - | No | Bandera de ausencia no programada | Binary | `0` (No / Planificada), `1` (Sí) | `1` | `1` si ausencia no autorizada previa | No | Internal | HR Operations | BR-06, BR-08 | FR-02, FR-16 |
| `is_absence_instance_start`|`SMALLINT`| - | No | Bandera de inicio de nuevo evento (S) | Binary | `0` (Continuación/No), `1` (Inicio S=1)| `1` | `1` si es día 1 de una secuencia | No | Internal | Derived/Logic Engine| BR-06, BR-08 | FR-02, FR-16 |

---

### 7.6 Entity: `fact_terminations`

#### Technical Metadata
* **Business Owner:** Global HR Director
* **Technical Owner:** People Analytics / HR Data Analyst
* **Data Steward:** People Operations Specialist
* **Primary Key:** `termination_id`
* **Grain:** Un registro por cada evento de desvinculación o egreso definitivo.
* **Refresh Frequency:** Diario (Nightly ETL)
* **Source System:** HRIS Termination Workflow
* **Estimated Rows:** ~1,200 registros históricos + acumulado futuro
* **Retention Policy:** 7 años
* **Contains PII:** No (Utiliza `employee_id` como clave asociativa)
* **GDPR Classification:** Confidential / Restricted

#### Column Specifications

| Campo | Tipo | PK/FK | Nullable | Descripción | Unidad | Dominio | Ejemplo | Regla de Validación | PII | Sensibilidad | Origen | BR Mapeadas | FR Mapeadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `termination_id` | `VARCHAR(15)` | PK | No | Identificador único del evento de egreso | Text | Pattern `TRM_\d{8}` | `TRM_20260512` | Único, No Nulo | No | Internal | HRIS Workflow | - | FR-04 |
| `employee_id` | `VARCHAR(10)` | FK | No | Clave foránea del empleado egresado | Text | `dim_employees.employee_id` | `EMP00851` | Debe existir en `dim_employees` | No | Confidential | HRIS Workflow | BR-01, BR-02 | FR-04, FR-10 |
| `termination_date` | `DATE` | - | No | Fecha oficial de desvinculación efectiva | YYYY-MM-DD | `2018-01-01` a `Current_Date` | `2026-05-12` | ≥ hire_date | No | Internal | HRIS Workflow | BR-02, BR-20 | FR-04, FR-12 |
| `termination_type` | `VARCHAR(20)` | - | No | Categoría legal de desvinculación | Code | `Voluntaria`, `Involuntaria`, `Jubilacion` | `Voluntaria` | En catálogo de salidas | No | Internal | HRIS Workflow | BR-02 | FR-04, FR-10 |
| `hris_exit_reason` | `VARCHAR(100)`| - | No | Motivo capturado en la entrevista HRIS | Text | Opciones del menú HRIS | `Desarrollo Profesional` | No Nulo | No | Confidential | HRIS Exit Form| BR-23 | FR-04, FR-09 |
| `proxy_reclassified_reason`|`VARCHAR(100)`| - | No | Causa raíz corregida mediante lógica proxy| Text | Categorías corregidas por datos | `Inconformidad Salarial (Proxy)`| Generado por regla BR-23 | No | Internal | Derived/Proxy Engine| BR-23 | FR-09 |
| `severance_cost_usd`|`DECIMAL(12,2)`| - | No | Costo de liquidación y legales pagados | USD | ≥ 0.00 | `4800.00` | Valor numérico no negativo | No | Restricted | Payroll Finance | BR-16, BR-17 | FR-26 |
| `notice_period_days`| `INT` | - | No | Días de preaviso otorgados por el empleado| Days | `0` a `90` | `15` | Entero ≥ 0 | No | Internal | HRIS Workflow | - | FR-04 |
| `is_regrettable_attrition`|`SMALLINT`| - | No | Marca si la salida perjudica al negocio | Binary | `0` (No deseada=No), `1` (Perjudicial=Sí)| `1` | `= 1` si Perf ≥ 4 y Voluntaria | No | Internal | Derived/HR Strategy| BR-03, BR-25 | FR-11 |

---

### 7.7 Entity: `fact_sla_events`

#### Technical Metadata
* **Business Owner:** VP of Operations
* **Technical Owner:** Analytics Engineering Lead
* **Data Steward:** Operations Service Manager
* **Primary Key:** `sla_event_id`
* **Grain:** Un registro por cada evento de incumplimiento o penalización de SLA.
* **Refresh Frequency:** Diario
* **Source System:** B2B Service Desk / Operational Incident Log
* **Estimated Rows:** 100 - 300 eventos por año
* **Retention Policy:** 5 años
* **Contains PII:** No
* **GDPR Classification:** Confidential

#### Column Specifications

| Campo | Tipo | PK/FK | Nullable | Descripción | Unidad | Dominio | Ejemplo | Regla de Validación | PII | Sensibilidad | Origen | BR Mapeadas | FR Mapeadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `sla_event_id` | `VARCHAR(15)` | PK | No | Identificador único de la penalización | Text | Pattern `SLA_\d{8}` | `SLA_20260701` | Único, No Nulo | No | Internal | Incident Log | - | FR-05 |
| `department_id` | `VARCHAR(10)` | FK | No | Departamento operativo involucrado | Text | `dim_departments.department_id` | `DEP_CLINICAL` | Debe existir en `dim_departments` | No | Internal | Incident Log | - | FR-05, FR-27 |
| `client_contract_id`|`VARCHAR(20)` | - | No | Identificador del contrato B2B cliente | Text | Pattern `CTR_\d{5}` | `CTR_99402` | Contrato B2B activo | No | Confidential | CRM / Contracts | BR-26 | FR-05 |
| `event_date` | `DATE` | - | No | Fecha de ocurrencia de la falla de SLA | YYYY-MM-DD | `2024-01-01` a `Current_Date` | `2026-07-01` | Fecha ISO válida | No | Internal | Incident Log | BR-14 | FR-05, FR-27 |
| `shift_id` | `VARCHAR(20)` | - | No | Turno operativo en que ocurrió el breach | Code | `Mañana`, `Tarde`, `Noche` | `Noche` | En catálogo de turnos | No | Internal | Incident Log | BR-14 | FR-05, FR-27 |
| `breach_type` | `VARCHAR(50)` | - | No | Tipo de incumplimiento de servicio | Code | `Demora en Respuesta`, `Falta de Cobertura`| `Falta de Cobertura`| En catálogo de incidencias | No | Internal | Incident Log | - | FR-05 |
| `hours_delayed` | `DECIMAL(4,2)`| - | No | Tiempo de retraso acumulado en el servicio| Hours | > 0.00 | `3.50` | Valor numérico positivo | No | Internal | Incident Log | - | FR-05 |
| `penalty_cost_usd`|`DECIMAL(10,2)`| - | No | Monto de la penalización financiera pagada| USD | > 0.00 | `1200.00` | Parámetro por defecto BR-15 | No | Restricted | Finance Contracts| BR-15 | FR-05, FR-27 |
| `attributed_to_staffing_deficit`|`SMALLINT`| - | No | Marca si la falla se debió a ausentismo | Binary | `0` (Falla Técnica), `1` (Déficit Personal)| `1` | `= 1` si ausentismo turno > 10% | No | Internal | Derived/Logic Engine| BR-14 | FR-05, FR-27 |

---

## 8. Derived Fields & Calculation Locus

Para mantener el desacoplamiento y evitar inconsistencias en el pipeline analítico, se especifican explícitamente los campos calculados, su fórmula determinista y sus dependencias directas:
```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ DERIVED FIELDS & CALCULATION LOCUS                                                                                      │
├────────────────────────────┬────────────────────────┬───────────────────────────────────┬───────────────────────────────┤
│ Target Attribute           │ Entity                 │ Transformation Logic / Formula    │ Source Attribute Dependencies │
├────────────────────────────┼────────────────────────┼───────────────────────────────────┼───────────────────────────────┤
│ annual_base_salary_usd     │ dim_employees          │ (base_salary_orig * 12) * fx_rate │ base_salary_orig, currency    │
│ fully_loaded_cost_usd      │ dim_employees          │ annual_base_salary_usd * 1.30     │ annual_base_salary_usd        │
│ overtime_hours             │ fact_attendance_logs   │ GREATEST(0, actual - planned)     │ actual_hours_worked, planned  │
│ is_absence_instance_start  │ fact_attendance_logs   │ Sequence lag logic (Day 1 start)  │ is_unplanned_absence, date    │
│ proxy_reclassified_reason  │ fact_terminations      │ Rule BR-23 (Comp/Burnout Proxy)   │ hris_exit_reason, salary, OT  │
│ is_regrettable_attrition   │ fact_terminations      │ Voluntaria AND Perf_Rating >= 4.0 │ termination_type, perf_rating │
│ attributed_to_staffing_def │ fact_sla_events        │ Shift_Absence_Rate > 10%          │ fact_attendance_logs, shift_id│
└────────────────────────────┴────────────────────────┴───────────────────────────────────┴───────────────────────────────┘
```

---
## 9. Data Quality Rules & Severity Matrix

Las reglas de calidad se clasifican en **4 niveles de severidad** para determinar la acción automática del pipeline de ingesta:
```text
┌──────────────────────────────────────────────────────────────────────────┐
│ DATA QUALITY SEVERITY LEVELS                                             │
├───────────────┬─────────────────────────────────┬────────────────────────┤
│ Severity Level│ Pipeline Action                 │ Alert Recipient        │
├───────────────┼─────────────────────────────────┼────────────────────────┤
│ CRITICAL      │ Immediate Pipeline Halt (Abort) │ Data Engineering Lead  │
│ HIGH          │ Quarantined Record Isolation    │ Data Steward           │
│ MEDIUM        │ Flagged Warning (Imputation)    │ Analytics Engineer     │
│ LOW           │ Logged Informational Audit      │ System Log Only        │
└───────────────┴─────────────────────────────────┴────────────────────────┘
```

### 9.1 Quality Validation Rules

1. **`DQ-INT-01` (CRITICAL - PK Uniqueness):** Rechazo inmediato y aborto del pipeline si existen duplicados en las claves primarias (`employee_id`, `department_id`, `position_id`, `benchmark_id`, `attendance_id`, `termination_id`, `sla_event_id`).
2. **`DQ-INT-02` (HIGH - Referential Integrity):** Aislar en tabla de cuarentena (`stg_quarantine_records`) todo registro transaccional en tablas de hechos (`fact_*`) con claves foráneas huérfanas sin correspondencia en dimensiones.
3. **`DQ-RNG-01` (CRITICAL - Salary Boundary):** Abortar si `annual_base_salary_usd` es ≤ 0.00 o > 300,000.00 USD.
4. **`DQ-RNG-02` (HIGH - Performance Rating Bounds):** Aislar si `performance_rating` no es `NULL` y se ubica fuera del intervalo [1.00, 5.00].
5. **`DQ-CNS-01` (HIGH - Temporal Sequence Coherence):** Aislar si `termination_date < hire_date`.
6. **`DQ-CNS-02` (MEDIUM - Active Status Alignment):** Generar advertencia si `is_active = 0` en `dim_employees` y no existe registro correspondiente en `fact_terminations`.
7. **`DQ-FMT-01` (LOW - Date Formatting Standard):** Convertir e informar si una fecha no cumple con el formato ISO 8601 (`YYYY-MM-DD`).

---

## 10. PII Classification & Data Privacy Matrix

En cumplimiento del Reglamento General de Protección de Datos (RGPD) en Europa y las normativas locales de protección de datos personales en LATAM, se establece la siguiente matriz de privacidad:
```text
┌──────────────────────────────────────────────────────────────────────────┐
│ PII & DATA SENSITIVITY CLASSIFICATION                                    │
├─────────────────┬───────────────────────────────┬────────────────────────┤
│ Sensitivity Tier│ Data Attributes Included      │ Security Control       │
├─────────────────┼───────────────────────────────┼────────────────────────┤
│ Restricted      │ Base Salary, Severance Cost   │ Role-Based Encryption  │
│ Confidential    │ First/Last Name, Email, Gender│ PII Anonymization Mask │
│ Internal        │ Dept, Position, Tenure, Status│ Standard Access Control│
│ Public          │ Aggregated Benchmarks / Totals│ No Restriction         │
└─────────────────┴───────────────────────────────┴────────────────────────┘
```

### Reglas de Enmascaramiento y Anonimización:
* **Anonimización en Vistas Analíticas:** Los campos de nivel *Confidential* (`first_name`, `last_name`, `work_email`) serán automáticamente enmascarados con asteriscos (ej. `C*** M***`) en las vistas globales de Power BI utilizadas por usuarios que no pertenezcan al rol directivo de HRBP.
* **Aislamiento de Información Restringida:** Los campos de nivel *Restricted* (Salarios individuales y liquidaciones) estarán protegidos mediante Seguridad a Nivel de Fila (RLS). Un HRBP solo podrá consultar salarios individuales de su unidad organizacional autorizada.

---

## 11. Validation Rules Summary

```sql
-- Reglas de Validación Ejecutables en SQL / Data Quality Pipeline

-- 1. Validación de Unicidad e Inmutabilidad de Empleados (CRITICAL)
ALTER TABLE dim_employees ADD CONSTRAINT chk_emp_id_format CHECK (employee_id SIMILAR TO 'EMP[0-9]{5}');

-- 2. Validación de Rangos de Salario y Desempeño (CRITICAL / HIGH)
ALTER TABLE dim_employees ADD CONSTRAINT chk_salary_positive CHECK (annual_base_salary_usd > 0);
ALTER TABLE dim_employees ADD CONSTRAINT chk_perf_range CHECK (performance_rating IS NULL OR (performance_rating BETWEEN 1.0 AND 5.0));

-- 3. Validación de Consistencia de Fechas en Egreso (HIGH)
ALTER TABLE fact_terminations ADD CONSTRAINT chk_term_date CHECK (termination_date >= '2015-01-01');

-- 4. Validación del Factor de Bradford en Asistencia (MEDIUM)
ALTER TABLE fact_attendance_logs ADD CONSTRAINT chk_hours_range CHECK (actual_hours_worked BETWEEN 0 AND 16);
```

---

## 12. Business Rules Mapping Matrix

La siguiente tabla garantiza la trazabilidad completa entre las 32 Reglas de Negocio (BR) definidas en el BRD v0.3.0 y los atributos específicos del Diccionario de Datos:

| Business Rule ID | Regla de Negocio (Resumen) | Entidad Responsable | Atributos de Datos Involucrados |
| :--- | :--- | :--- | :--- |
| **BR-01** | Definición de Empleado Activo | `dim_employees` | `is_active`, `hire_date` |
| **BR-02** | Fórmula de Rotación Voluntaria | `fact_terminations` | `termination_type`, `termination_date` |
| **BR-03** | Clasificación de High-Performer (≥ 4.0) | `dim_employees` | `performance_rating`, `is_critical_position` |
| **BR-06** | Fórmula Factor de Bradford (B = S² × D) | `fact_attendance_logs` | `is_unplanned_absence`, `is_absence_instance_start` |
| **BR-07** | Umbrales de Riesgo de Bradford | `fact_attendance_logs` | Metodología de cálculo sobre `absence_type` |
| **BR-08** | Definición de Instancia de Ausencia (S) | `fact_attendance_logs` | `is_absence_instance_start` |
| **BR-09** | Exclusiones de Ausentismo (Vacaciones) | `fact_attendance_logs` | `absence_type` |
| **BR-10** | Fórmula de Compa-Ratio | `dim_employees` / `dim_salary_benchmarks` | `annual_base_salary_usd`, `market_midpoint_salary_usd` |
| **BR-11** | Alcance de Salario Fijo Base | `dim_employees` | `base_salary_orig`, `annual_base_salary_usd` |
| **BR-12** | Estándar de Conversión de Monedas | `dim_employees` | `salary_currency_orig`, `country_code` |
| **BR-13** | Marcadores Salariales de Mercado | `dim_salary_benchmarks` | `market_midpoint_salary_usd`, `effective_year` |
| **BR-14** | Atribución de Falla por Déficit de Personal | `fact_sla_events` | `attributed_to_staffing_deficit`, `shift_id` |
| **BR-15** | Costo Fijo de Penalización SLA ($1,200 USD) | `fact_sla_events` | `penalty_cost_usd` |
| **BR-16** | Factor Multiplicador de Vacancia (1.5x) | `dim_employees` / `dim_positions` | `fully_loaded_cost_usd`, `market_scarcity_index` |
| **BR-17** | Cargas Prestacionales (30%) | `dim_employees` | `fully_loaded_cost_usd` |
| **BR-20** | Intervalos de Antigüedad (Tenure) | `dim_employees` | `hire_date` (Cálculo dinámico de antigüedad) |
| **BR-21** | Alerta de Desgaste por Horas Extra (> 30h) | `fact_attendance_logs` | `overtime_hours`, `date_key` |
| **BR-22** | Umbral de Anonimización (≤ 5 empleados) | Visualización BI | Agregación dinámica sobre `department_id` |
| **BR-23** | Reclasificación Proxy de Razones de Salida | `fact_terminations` | `hris_exit_reason`, `proxy_reclassified_reason` |
| **BR-24** | Escala Estándar de Desempeño (1.0 - 5.0) | `dim_employees` | `performance_rating` |
| **BR-25** | Atribución de Pérdida de Talento Clave | `fact_terminations` | `is_regrettable_attrition` |
| **BR-26** | Riesgo en Renovación de Contratos B2B | `fact_sla_events` | `client_contract_id`, `penalty_cost_usd` |
| **BR-31** | Sesgo de Evaluación del Líder | `dim_employees` | `performance_rating`, `position_id` |
| **BR-32** | Alerta de Cobertura de Emergencia | `dim_departments` | `target_headcount` vs. `is_active` |

---

## 13. Source Systems Architecture & Lineage

El linaje de datos (*Data Lineage*) describe el flujo de transformación de los atributos desde los sistemas origen hasta las tablas analíticas:

```text
[ HRIS Core System ] ──────────────► ETL Pipeline ──► dim_employees
[ HRIS Org Catalog ] ──────────────► ETL Pipeline ──► dim_departments
[ Job Architecture Catalog ] ──────► ETL Pipeline ──► dim_positions
[ Market Intelligence Studies ] ───► ETL Pipeline ──► dim_salary_benchmarks
[ Time & Attendance Logs ] ────────► ETL Pipeline ──► fact_attendance_logs
[ Exit Interview Records ] ────────► ETL Pipeline ──► fact_terminations
[ B2B Incident Helpdesk ] ─────────► ETL Pipeline ──► fact_sla_events
```

---

## 14. Data Refresh & ETL Strategy

* **Frecuencia de Carga:** Carga nocturna automatizada (*Nightly Batch*) de lunes a domingo.
* **Orden de Carga:** Procesamiento inicial de dimensiones (`dim_departments`, `dim_positions`, `dim_employees`, `dim_salary_benchmarks`) seguido por tablas de hechos (`fact_attendance_logs`, `fact_terminations`, `fact_sla_events`).
* **SCD Type 2:** Mantenimiento de vigencia histórica de salarios y puestos en `dim_employees` (`is_current_row`).
* **Validación Automática:** Filtro de calidad antes de la inserción y derivación de registros anómalos para auditoría.

---

## 15. Future Fields & Extensibility

Las siguientes columnas quedan reservadas para incorporación en la base de datos en las versiones v1.0 y v2.0 de la plataforma:

- `exit_interview_sentiment_score` (DECIMAL(3,2)): Puntuación de sentimiento sobre el texto libre de entrevistas de salida (v1.0).
- `internal_flight_risk_index_v2` (DECIMAL(5,4)): Puntuación analítica de supervivencia Kaplan-Meier (v1.0).
- `engagement_survey_score` (DECIMAL(3,2)): Resultado individual de encuestas de clima laboral (v2.0).

---

## 16. Revision History

| Version | Date | Author | Description of Changes | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **v0.1.0** | 2026-07-15 | People Analytics Specialist | Borrador inicial de campos básicos | Project Team |
| **v0.2.0** | 2026-07-20 | HR Data Analyst | Incorporación de banderas PII y mapeo FR/BR | HR Tech Board |
| **v0.3.0** | 2026-07-29 | People Analytics Lead | Alineación con BRD v0.3.0 y tablas analíticas | C-Suite Sponsor |
| **v0.4.0** | 2026-08-04 | People Analytics / HR Data Analyst | Rediseño integral como Data Contract: 7 entidades completas, Fichas Técnicas, DQ Rules, Sensibilidad y Linaje | Executive Committee |


