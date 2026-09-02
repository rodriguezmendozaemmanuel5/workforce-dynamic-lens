# TECHNICAL ARCHITECTURE DOCUMENT
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & WORKFORCE DYNAMICS SOLUTION

**Document Version:** v0.5.0  
**Target Audience:** People Analytics Leaders, HR Data Analysts, BI Developers, Technical Recruiters, Solution Reviewers  
**Project Author:** Emmanuel Rodríguez Mendoza  
**Professional Role:** People Analytics / HR Data Analyst  
**Project:** Workforce Dynamic Lens  
**Date:** 2026-08-08  
**Status:** Architecture Design Baseline – Completed (v0.5.0)  

---

## 1. Executive Overview & Architectural Scope

El **Technical Architecture Document (v0.5.0)** define el blueprint técnico integral para la plataforma analítica **Workforce Dynamic Lens** de MedTech Global Solutions. Este documento traduce los requerimientos funcionales, analíticos, financieros y de gobierno definidos en el *Business Case* (v0.3.0), *BRD* (v0.3.0), *Data Dictionary* (v0.4.0) y *KPI Catalog* (v0.5.0) en una arquitectura de datos, modelado relacional y capas de visualización ejecutiva.

### 1.1 Architectural Purpose & Boundaries
El propósito de esta arquitectura es proporcionar una solución analítica desacoplada, escalable y auditable para procesar, validar y analizar datos operacionales y de talento humano de **4,500 colaboradores activos** e históricos en LATAM y Europa. La plataforma ingesta datos de RR. HH., asistencia, nómina y servicios B2B, ejecutando validaciones de calidad, modelado dimensional en estrella en PostgreSQL, vistas analíticas en SQL y tableros interactivos de soporte a la decisión en Power BI.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ ARCHITECTURAL BOUNDARIES & METRICS TRACEABILITY                          │
├──────────────────────────────┬───────────────────────────────────────────┤
│ Target Population            │ 4,500 Active Employees + 1,200 Historical │
│ Database Engine (Warehouse)  │ PostgreSQL 16+ (Dimensional Schema)       │
│ Data Prep & ETL Engine       │ Python 3.11+ / SQLAlchemy / Pandas        │
│ Analytics & Views Layer      │ ANSI SQL / CTEs / Window Functions        │
│ Semantic & BI Suite          │ Microsoft Power BI Pro (DAX Measures)     │
│ Security & Privacy Standard  │ Row-Level Security (RLS) / GDPR / LATAM   │
└──────────────────────────────┴───────────────────────────────────────────┘
```

---

## 2. Enterprise Architecture Principles

La arquitectura de la solución se rige por ocho principios fundamentales de análisis y gobierno de datos:

1. **Separation of Concerns (SoC):** Desacoplamiento estricto entre la capa de extracción/preparación (*Python Ingestion*), almacenamiento dimensional (*PostgreSQL Data Warehouse*), capas de agregación (*SQL Analytics Views*) y la capa de consumo ejecutivo (*Power BI*).
2. **Layered Architecture:** Estructuración modular en capas (*Raw, Staging, Core Dimensional Schema, Analytical Mart Views, Presentation*) para garantizar trazabilidad y mantenibilidad.
3. **Data Quality at Ingress:** Validación estricta del contrato de datos antes de permitir la inserción en el modelo relacional, rechazando anomalías o derivándolas a cuarentena.
4. **Historical Traceability (SCD Type 2):** Preservación del historial de variaciones salariales y organizacionales en colaboradores mediante vigencias temporales (`row_effective_date`, `row_expiration_date`, `is_current_row`).
5. **Security by Design:** Implementación de controles de acceso basados en roles (*RBAC*) y seguridad a nivel de fila (*RLS*) para aislar información sensible por departamento.
6. **Privacy by Design:** Anonimización y enmascaramiento automático de Información de Identificación Personal (PII) en cumplimiento del RGPD europeo y regulaciones de LATAM.
7. **Deterministic Reproducibility:** Semillas aleatorias fijas (`seed=42`) en la generación y preparación de datos sintéticos para asegurar reproducibilidad total.
8. **Business Metric Auditability:** Trazabilidad matemática directa entre requerimientos de negocio, lógica SQL, medidas DAX y visualizaciones ejecutivas.

---

## 3. High-Level Solution Architecture

### 3.1 Layer Diagram
```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PRESENTATION & EXECUTIVE BI LAYER                                                               │
│ └─► Microsoft Power BI Suite (Boardroom Overview, HRBP Action Center, Financial What-If Sim)    │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ ANALYTICS & SEMANTIC LAYER                                                                      │
│ ├─► Power BI DAX Semantic Layer (Time Intelligence, Dynamic Rates, Financial Multipliers)       │
│ └─► SQL Analytical Views (Headcount Snapshots, Monthly Turnover, Bradford Score, Compa-Ratio)   │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ DATA WAREHOUSE LAYER (PostgreSQL 16+ Engine)                                                    │
│ ├─► Core Star Schema (dim_employees, dim_departments, dim_positions, dim_salary_benchmarks)     │
│ └─► Fact Tables (fact_attendance_logs, fact_terminations, fact_sla_events, dim_date)             │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ INGESTION & DATA QUALITY LAYER                                                                  │
│ ├─► Python Data Preparation & ETL Engine (SQLAlchemy, Pandas, NumPy)                            │
│ └─► Data Quality Validation Suite (Referential Integrity, Null Controls, Range Bounds)          │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SOURCE DATA LAYER                                                                               │
│ └─► HRIS Master Data / Clock-In Logs / Market Salary Feeds / B2B SLA Service Desk Logs          │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 End-to-End Analytical Flow
```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ END-TO-END ANALYTICAL FLOW                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│  [ SOURCE DATA ] ──► [ DATA PREPARATION & ETL ] ──► [ POSTGRESQL STAR SCHEMA ] ──► [ SQL VIEWS & POWER BI ]     │
│                                                                                                                 │
│  ┌──────────────┐       ┌────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────┐  │
│  │ HRIS Core    │──────►│ Python Extract & Clean │──────►│  schema: people_analytic│──────►│ Power BI        │  │
│  │ Employee Feed│       │ (SQLAlchemy & Pandas)  │       │  - dim_employees (SCD2) │       │ Semantic Model  │  │
│  └──────────────┘       └───────────┬────────────┘       │  - dim_departments      │       │ (DAX Measures)  │  │
│  ┌──────────────┐                   │                    │  - dim_positions        │       └────────┬────────┘  │
│  │ Time Tracker │                   ▼                    │  - dim_salary_benchmarks│                │           │
│  │ Clock-In Logs│       ┌────────────────────────┐       │  - dim_date (2012-2030) │                ▼           │
│  └──────────────┘       │ Data Quality Gate      │       │  - fact_attendance_logs │       ┌─────────────────┐  │
│  ┌──────────────┐       │ (Referential Checks)   │       │  - fact_terminations    │       │ Boardroom       │  │
│  │ SLA Incidents│       └───────────┬────────────┘       │  - fact_sla_events      │       │ Executive View  │  │
│  │ Desk Log     │                   │                    └────────────┬────────────┘       ├─────────────────┤  │
│  └──────────────┘                   ▼                                 │                    │ HRBP Action     │  │
│  ┌──────────────┐       ┌────────────────────────┐                    ▼                    │ Center          │  │
│  │ Salary Market│       │ Clean Relational Load  │       ┌─────────────────────────┐       ├─────────────────┤  │
│  │ Benchmarks   │       │ (PostgreSQL Database)  │       │ Analytical SQL Views    │──────►│ Financial       │  │
│  └──────────────┘       └────────────────────────┘       │ (Aggregations & Marts)  │       │ What-If Sim     │  │
│                                                          └─────────────────────────┘       └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Source Systems & Ingestion Specifications

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SOURCE DATA CATALOG                                                                                                    │
├─────────────────────────┬──────────────────────────────┬───────────────────┬─────────────────────┬─────────────────────┤
│ System Name             │ Business Domain              │ Data Interface    │ Extract Format      │ Sync Frequency      │
├─────────────────────────┼──────────────────────────────┼───────────────────┼─────────────────────┼─────────────────────┤
│ HRIS Core System        │ Employee Master & Org        │ Database / CSV    │ Structured CSV/Table│ Daily Batch (01:00) │
│ Time & Attendance Log   │ Clock-In & Overtime          │ Time Clock DB     │ Daily Log Table     │ Daily Batch (01:30) │
│ HRIS Termination Flow   │ Exit & Severance Records     │ HR Workflow DB    │ Transactional Feed  │ Daily Batch (01:15) │
│ External Salary Intel   │ Market Salary Benchmarks     │ Static Feed / CSV │ Tabular File        │ Bi-Annually         │
│ B2B Incident Desk (CRM) │ Contract SLA Breaches        │ Service Desk API  │ Incident Event Feed │ Daily Batch (01:45) │
└─────────────────────────┴──────────────────────────────┴───────────────────┴─────────────────────┴─────────────────────┘
```

---

## 5. Data Flow & Data Lineage

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ END-TO-END DATA LINEAGE                                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                 │
│  [ SOURCE SYSTEMS ] (HRIS Master / Clock-In / Salary Studies / Incident Desk)                                  │
│         │                                                                                                       │
│         ▼                                                                                                       │
│  [ EXTRACTION & STAGING ] (Pandas DataFrames / In-Memory Buffers)                                               │
│         │                                                                                                       │
│         ▼                                                                                                       │
│  [ DATA QUALITY ENGINE ] (Validation Gate: PK/FK, Nulls, Ranges, Date Boundaries)                              │
│         │                                                                                                       │
│         ▼                                                                                                       │
│  [ CORE DATA WAREHOUSE ] (schema: people_analytics)                                                             │
│         ├─► dim_departments, dim_positions, dim_salary_benchmarks, dim_date                                    │
│         ├─► dim_employees (SCD Type 2: historical tracking & is_current_row)                                    │
│         └─► fact_attendance_logs, fact_terminations, fact_sla_events                                            │
│         │                                                                                                       │
│         ▼                                                                                                       │
│  [ ANALYTICAL VIEWS LAYER ] (SQL Marts: monthly_headcount_snapshot, monthly_attrition_summary)                  │
│         │                                                                                                       │
│         ▼                                                                                                       │
│  [ POWER BI SEMANTIC MODEL ] (DAX Measures: Bradford Score, Turnover Rate, Compa-Ratio, Total Turnover Cost)   │
│         │                                                                                                       │
│         ▼                                                                                                       │
│  [ EXECUTIVE DASHBOARDS ] (Boardroom Overview, HRBP Action Center, Financial What-If Simulator)                │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Data Warehouse Architecture & Star Schema Layout

### 6.1 Database Object Naming Conventions

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ OBJECT NAMING CONVENTIONS                                                │
├─────────────────────────┬──────────────────────┬─────────────────────────┤
│ Layer / Object Type     │ Prefix / Pattern     │ Example                 │
├─────────────────────────┼──────────────────────┼─────────────────────────┤
│ Dimension Tables        │ dim_*                │ dim_employees           │
│ Fact Tables             │ fact_*               │ fact_attendance_logs    │
│ Analytics Views         │ view_*               │ view_monthly_headcount  │
│ Python ETL Modules      │ python/etl/*         │ load_dimensions.py      │
│ Validation Scripts      │ validation.py        │ validation_queries.sql  │
│ DAX Measures Group      │ [Measure_Name]       │ [Voluntary_Attrition %] │
└─────────────────────────┴──────────────────────┴─────────────────────────┘
```

### 6.2 Star Schema Entity-Relationship Layout

```text
                    ┌────────────────────────┐
                    │    dim_departments     │
                    │ ────────────────────── │
                    │ PK department_sk       │
                    └───────────┬────────────┘
                                │ 1:N
                                ▼
┌───────────────────────┐   ┌────────────────────────┐   ┌────────────────────────┐
│     dim_positions     │───►│     dim_employees      │◄──│ dim_salary_benchmarks  │
│ ───────────────────── │   │ ────────────────────── │   │ ────────────────────── │
│ PK position_sk        │1:N│ PK employee_sk         │1:N│ PK benchmark_sk        │
└───────────┬───────────┘   │ FK department_sk       │   │ FK position_sk         │
            │               │ FK position_sk         │   └────────────────────────┘
            │               └───────────┬────────────┘
            │ 1:N                       │ 1:N
            │             ┌─────────────┴─────────────┐
            │             │                           │
            ▼             ▼                           ▼
┌───────────────────────┐ ┌─────────────────────┐ ┌────────────────────────┐
│ fact_attendance_logs  │ │  fact_terminations  │ │    fact_sla_events     │
│ ───────────────────── │ │ ─────────────────── │ │ ────────────────────── │
│ PK attendance_id      │ │ PK termination_id   │ │ PK sla_event_id        │
│ FK employee_sk        │ │ FK employee_sk      │ │ FK department_sk       │
│ FK date_key (dim_date)│ │ FK date_key         │ │ FK date_key            │
└───────────────────────┘ └─────────────────────┘ └────────────────────────┘
```

### 6.3 Indexing Strategy
* **Primary Key Indexing:** B-Tree Indexes automáticos sobre todas las claves primarias (`employee_sk`, `department_sk`, etc.).
* **Foreign Key Indexing:** B-Tree Indexes sobre claves foráneas en tablas de hechos (`fact_attendance_logs(employee_sk)`, `fact_terminations(employee_sk)`).
* **Composite Temporal Indexing:** Índice compuesto B-Tree sobre `fact_attendance_logs(employee_sk, date_key)` y filtro parcial en ausentismo no programado para acelerar el cálculo del Factor de Bradford (`BR-06`).

---

## 7. ETL Engine, Data Contracts & Transformation Logic

El pipeline ETL está implementado en **Python 3.11** utilizando `SQLAlchemy`, `Pandas` y `NumPy`.

### 7.1 Data Contract Validation Gate
Antes de persistir los datos en PostgreSQL, el pipeline valida la estructura y reglas de calidad:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ DATA CONTRACT ENFORCEMENT CHECKS                                         │
├───────────────────────────────┬──────────────────────────────────────────┤
│ Check Category                │ Validation Enforcement Action            │
├───────────────────────────────┼──────────────────────────────────────────┤
│ Primary Key Uniqueness        │ Abort execution if duplicate PK detected │
│ Foreign Key Referential       │ Enforce referential integrity in DB      │
│ Nullability Constraints       │ Rejects rows with NULLs in required fields│
│ Value Range Bounds            │ Verifies Salary > 0 and Rating in [1, 5] │
│ Accepted Categorical Values   │ Validates ISO-3 countries & Gender codes │
│ Date Sequence Coherence       │ Enforces Termination Date >= Hire Date   │
└───────────────────────────────┴──────────────────────────────────────────┘
```

### 7.2 Core Transformation Logic
* **Currency Standardization (`FR-08`):**  
  `annual_base_salary_usd = (base_salary_orig * 12) * fx_rate`
* **Exit Reason Proxy Reclassification (`BR-23` / `FR-09`):**
  * *Inconformidad Salarial (Proxy):* Si `hris_exit_reason = 'Desarrollo Profesional'` y `compa_ratio < 0.85` $\rightarrow$ `'Inconformidad Salarial (Proxy)'`
  * *Burnout / Agotamiento (Proxy):* Si `hris_exit_reason = 'Desarrollo Profesional'` y `overtime_hours_30d > 30` $\rightarrow$ `'Burnout / Agotamiento (Proxy)'`
* **SCD Type 2 Maintenance:**  
  Control de vigencia temporal en `dim_employees` asignando `row_effective_date`, `row_expiration_date` e `is_current_row = TRUE/FALSE`.

---

## 8. Data Quality Layer & Logging Strategy

### 8.1 Logging Framework
El pipeline registra eventos y métricas de ejecución en formato JSON estructurado:

```json
{
  "timestamp": "2026-08-14T02:15:30Z",
  "pipeline_step": "etl_load_dimensions",
  "log_level": "INFO",
  "execution_time_seconds": 12.4,
  "rows_processed": 4933,
  "rows_rejected": 0,
  "dq_validation_status": "PASSED_100_PERCENT",
  "environment": "local_analytics"
}
```

### 8.2 Operational Health Checks
* **Pipeline Status:** Estado de carga por tabla de hechos y dimensiones.
* **Integrity Audit:** Queries de verificación automáticas (`14_validation_queries.sql`) para asegurar 0 violaciones de integridad referencial.
* **Row Count & Balance:** Verificación de consistencia entre empleados activos, terminados y registros de asistencia.

---

## 9. Advanced Analytics Layer & SQL Views

La capa analítica intermedia consolida consultas complejas para optimizar el rendimiento de Power BI:

1. **`view_monthly_headcount_snapshot`:** Agregación mensual de plantilla activa por departamento, excluyendo colaboradores desvinculados (`is_active = FALSE`).
2. **`view_monthly_attrition_summary`:** Agrupación de salidas voluntarias, rotación de personal de alto desempeño (*Regrettable Attrition*) y costos directos de indemnización.
3. **`view_absenteeism_bradford`:** Consolidación de instancias de ausencia ($S$) y días acumulados ($D$) para el cálculo del Factor de Bradford.
4. **`view_compa_ratio_distribution`:** Distribución del ratio salarial comparado contra el punto medio de mercado (`dim_salary_benchmarks`).

---

## 10. Security, Privacy & Compliance Architecture

### 10.1 Access Control & Row-Level Security (RLS)
* **Role-Based Access Control (RBAC):** Definición de perfiles de acceso analítico (`role_csuite`, `role_hrbp`, `role_ops`).
* **Row-Level Security (Power BI / SQL):** Filtros de seguridad por departamento para que cada HRBP visualice exclusivamente su área asignada.

### 10.2 PII Anonymization Matrix
```text
┌──────────────────────────────────────────────────────────────────────────┐
│ PII ANONYMIZATION MATRIX                                                 │
├─────────────────┬───────────────────────────────┬────────────────────────┤
│ Sensitivity Tier│ Attributes                    │ Handling Rule          │
├─────────────────┼───────────────────────────────┼────────────────────────┤
│ Restricted      │ Base Salary, Severance        │ Masked / RLS Control   │
│ Confidential    │ First/Last Name, Work Email   │ Anonymized in Reports  │
│ Internal        │ Department, Position, Tenure  │ Unmasked for Analytics │
└─────────────────┴───────────────────────────────┴────────────────────────┘
```

---

## 11. Technology Stack Catalog

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ COMPREHENSIVE TECHNOLOGY STACK CATALOG                                                                                 │
├─────────────────────────┬───────────────────────────────┬─────────────────┬──────────────┬─────────────────────────────┤
│ Architecture Layer      │ Technology / Library          │ Language        │ Vendor       │ Role in Project             │
├─────────────────────────┼───────────────────────────────┼─────────────────┼──────────────┼─────────────────────────────┤
│ Database (Warehouse)    │ PostgreSQL 16+                │ ANSI SQL / DDL  │ Open Source  │ Relational Star Schema      │
│ Data Preparation & ETL  │ SQLAlchemy / Pandas / NumPy   │ Python 3.11     │ Open Source  │ Extraction, Clean & Load    │
│ Data Quality & Contract │ Custom Quality Suite          │ Python 3.11     │ Open Source  │ Integrity Validation Gate   │
│ Analytics & Aggregations│ PostgreSQL Views & Queries    │ SQL             │ Open Source  │ Analytical Aggregations     │
│ Business Intelligence   │ Microsoft Power BI Pro        │ DAX / M         │ Microsoft    │ Executive Dashboards & BI   │
│ Version Control         │ Git & GitHub                  │ Markdown / YAML │ GitHub       │ Repository & Documentation  │
│ Workspace & IDE         │ VS Code / Jupyter Notebooks   │ Python / SQL    │ Microsoft    │ Development Environment     │
└─────────────────────────┴───────────────────────────────┴─────────────────┴──────────────┴─────────────────────────────┘
```

---

## 12. Testing & Quality Assurance Strategy

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ TESTING STRATEGY FRAMEWORK                                               │
├───────────────────────┬──────────────────────────────────────────────────┤
│ Test Level            │ Verification Scope                               │
├───────────────────────┼──────────────────────────────────────────────────┤
│ 1. Unit Tests         │ Validar funciones de transformación en Python   │
│ 2. Pipeline Tests     │ Ejecución completa de carga ETL sin errores      │
│ 3. Data Quality Tests │ Cumplimiento de reglas de contrato de datos      │
│ 4. SQL Schema Tests   │ Integridad de claves PK/FK y restricciones CHECK │
│ 5. Metric Validation  │ Conciliación de KPIs entre SQL y DAX en Power BI │
│ 6. Performance Tests  │ Tiempo de respuesta de consultas < 500 ms        │
└───────────────────────┴──────────────────────────────────────────────────┘
```

---

## 13. Architecture Decision Records (ADRs)

### ADR-001: Selection of PostgreSQL 16+ as Relational Data Warehouse Engine
* **Status:** Approved
* **Context:** Se requiere un motor relacional robusto, con soporte completo para ANSI SQL, funciones de ventana, restricciones de integridad y RLS.
* **Decision:** Seleccionar PostgreSQL 16+.
* **Consequences:** Excelente rendimiento, cero costo de licenciamiento y compatibilidad nativa con Python y Power BI.

### ADR-002: Implementation of Kimball Dimensional Star Schema
* **Status:** Approved
* **Context:** La capa de reportería requiere consultas rápidas sobre rotación, ausentismo y salarios.
* **Decision:** Diseñar un Esquema en Estrella con 4 dimensiones y 3 tablas de hechos.
* **Consequences:** Simplifica las medidas DAX en Power BI y optimiza el filtrado analítico.

### ADR-003: Adoption of Python 3.11 for Data Preparation and ETL
* **Status:** Approved
* **Context:** Se requiere un lenguaje estándar y reproducible para generación sintética, limpieza y validación de calidad.
* **Decision:** Adoptar Python 3.11 con Pandas y SQLAlchemy.
* **Consequences:** Código modular, fácil de mantener y trazable mediante Git.

### ADR-004: Selection of Microsoft Power BI as Executive BI Platform
* **Status:** Approved
* **Context:** La alta dirección requiere tableros visuales interactivos y simulación What-If.
* **Decision:** Seleccionar Power BI Pro.
* **Consequences:** Integración fluida con el modelo dimensional, lenguaje DAX potente para KPIs dinámicos y adopción ejecutiva inmediata.

### ADR-005: Pre-Calculated Analytical Views over Heavy Real-Time Joins
* **Status:** Approved
* **Context:** Agregaciones mensuales de plantilla y ausentismo pueden sobrecargar la capa de visualización si se ejecutan en tiempo real.
* **Decision:** Crear vistas analíticas especializadas en SQL dentro del esquema `people_analytics`.
* **Consequences:** Respuestas sub-segundo en Power BI y lógica analítica centralizada en la base de datos.

### ADR-006: Nightly Batch ETL Strategy
* **Status:** Approved
* **Context:** Los eventos de talento humano y asistencia se consolidan en ciclos diarios.
* **Decision:** Ejecución de pipeline ETL en lotes programados.
* **Consequences:** Mínimo consumo de recursos y estabilidad en los snapshots analíticos.

---

### Architecture Baseline Sign-Off

```text
[✓] ARCHITECTURE DESIGN BASELINE APPROVED

Project Author: Emmanuel Rodríguez Mendoza
Professional Role: People Analytics / HR Data Analyst
Date: 2026-08-08
```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ COMPREHENSIVE TECHNOLOGY STACK CATALOG                                                                                 │
├─────────────────────────┬───────────────────────────────┬─────────────────┬──────────────┬─────────────────────────────┤
│ Architecture Layer      │ Technology / Framework        │ Language        │ Vendor       │ License / Role              │
├─────────────────────────┼───────────────────────────────┼─────────────────┼──────────────┼─────────────────────────────┤
│ Data Warehouse          │ PostgreSQL 16+                │ ANSI SQL / PLpg │ Open Source  │ Relational DW Engine        │
│ ETL / Data Pipeline     │ SQLAlchemy / Pandas / NumPy   │ Python 3.11     │ Open Source  │ Data Extraction & Prep      │
│ Data Quality            │ Custom Validation Suite       │ Python 3.11     │ Open Source  │ Data Contract Enforcement   │
│ Analytical Layer        │ PostgreSQL Analytical Views   │ ANSI SQL / CTEs │ Open Source  │ Workforce Metrics & Views   │
│ Business Intelligence   │ Microsoft Power BI Pro        │ DAX / M         │ Microsoft    │ Enterprise Visualization    │
│ Version Control & CI/CD │ Git / GitHub Actions          │ YAML / Bash     │ GitHub       │ Code & Workflow Automation  │
│ IDE & Workspace         │ VS Code / Jupyter Lab         │ Python / SQL    │ Microsoft    │ Development Environment     │
└─────────────────────────┴───────────────────────────────┴─────────────────┴──────────────┴─────────────────────────────┘
```

---

## 14. Testing & Quality Assurance Strategy

La estrategia de pruebas abarca seis dimensiones automatizadas mediante `pytest` y scripts de validación en SQL:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ TESTING STRATEGY FRAMEWORK                                               │
├───────────────────────┬──────────────────────────────────────────────────┤
│ Test Level            │ Verification Scope & Framework                   │
├───────────────────────┼──────────────────────────────────────────────────┤
│ 1. Unit Tests         │ Test individual Python functions and transforms │
│ 2. Integration Tests  │ Test end-to-end ELT pipeline with test DB        │
│ 3. Data Quality Tests │ Enforce Data Contract rules on ingested data     │
│ 4. SQL Tests          │ Validate Star Schema constraints, PK/FK integrity│
│ 5. DAX Reconciliation │ Validate 100% metric parity between SQL and DAX  │
│ 6. Performance Tests  │ Verify query response < 500ms and ETL < 10 mins  │
└───────────────────────┴──────────────────────────────────────────────────┘
```

---

## 15. Versioning & Artifact Governance Strategy

* **Semantic Versioning (Software/Pipelines):** Formato `vMAJOR.MINOR.PATCH` (ej. Pipeline `v0.6.0`).
* **SQL DDL & Views Versioning:** Scripts ordenados secuencialmente en `sql/` con control de cambios estricto.
* **Dataset Versioning:** Identificados por marcas de tiempo en la capa de datos.
* **Repository Git Tags:** Tags formales creadas en cada release de arquitectura.

---

## 16. Technical Risk Register & Mitigation Matrix

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TECHNICAL RISK REGISTER                                                                                                │
├──────────────────────────────┬────────────┬─────────────┬──────────────────────────────────────────────────────────────┤
│ Technical Risk               │ Severity   │ Probability │ Mitigation Strategy                                          │
├──────────────────────────────┼────────────┼─────────────┼──────────────────────────────────────────────────────────────┤
│ HRIS System Unavailability   │ High       │ Medium      │ Retry mechanism with exponential backoff & cached extracts   │
│ Source API Timeout           │ Medium     │ Medium      │ Session timeout parameterization and chunked batch extraction │
│ PostgreSQL Database Failure  │ High       │ Low         │ Point-In-Time Recovery (PITR) & automated daily WAL backups  │
│ Metric Calculation Disparity │ High       │ Medium      │ Automated SQL vs DAX reconciliation test suite in CI/CD      │
│ Source Schema Drift / Change │ High       │ Low         │ Strict Data Contract validation layer aborting bad schemas   │
└──────────────────────────────┴────────────┴─────────────┴──────────────────────────────────────────────────────────────┘
```

---

## 17. Non-Functional Requirements & Performance SLAs

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ NON-FUNCTIONAL REQUIREMENTS & PERFORMANCE SLAS                           │
├───────────────────────────────┬──────────────────────────────────────────┤
│ Metric Category               │ SLA Target Performance                   │
├───────────────────────────────┼──────────────────────────────────────────┤
│ ETL Pipeline Execution Time   │ < 10 Minutes (Nightly Execution)         │
│ Power BI Dashboard Load Time  │ < 3 Seconds (Interactive Queries)        │
│ SQL View Execution Speed      │ < 500 ms (Indexed Dimensional Queries)   │
│ Metric Reconciliation Parity  │ 100.0% Exact Parity (SQL vs. DAX)        │
│ System Availability           │ 99.5% Uptime (Business Hours)            │
│ Data Backup Recovery (RTO)    │ < 4 Hours (Recovery Time Objective)      │
│ Data Loss Boundary (RPO)      │ < 24 Hours (Recovery Point Objective)    │
└───────────────────────────────┴──────────────────────────────────────────┘
```

---

## 18. Disaster Recovery & Resilience Policy

* **Automated Daily Backups:** `pg_dump` ejecutado de forma automatizada a las 04:00 AM UTC con retención de 30 días.
* **Point-In-Time Recovery (PITR):** Archivado continuo de logs Write-Ahead (WAL) en PostgreSQL.

---

## 19. Phased Technical Deployment Roadmap

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ TECHNICAL DEPLOYMENT ROADMAP                                             │
├──────────┬─────────────────────────────┬─────────────────────────────────┤
│ Phase    │ Focus Area                  │ Technical Deliverable           │
├──────────┼─────────────────────────────┼─────────────────────────────────┤
│ Phase 1  │ Database & Schema Setup     │ PostgreSQL DDL & Star Schema    │
│ Phase 2  │ Ingestion & Data Quality    │ Python ELT & Validation Engine  │
│ Phase 3  │ Analytical Views & SQL Logic│ Dynamic SQL Views & Aggregations│
│ Phase 4  │ Executive Visualizations    │ Power BI Suite & RLS Security   │
└──────────┴─────────────────────────────┴─────────────────────────────────┘
```

---

## 20. Architecture Decision Records (ADRs) & Sign-Off

### ADR-001: Selection of PostgreSQL 16+ as Primary Data Warehouse Engine
* **Status:** Approved
* **Context:** La plataforma requiere un motor relacional robusto, compatible con ANSI SQL, soporte para JSONB y capacidades avanzadas de encriptación y RLS.
* **Decision:** Seleccionar PostgreSQL 16+ como motor primario de almacenamiento.
* **Consequences:** Excelente rendimiento sin costo de licencias software, compatibilidad total con Python/Power BI y ruta de migración transparente hacia Azure Database for PostgreSQL.

### ADR-002: Implementation of Dimensional Star Schema over ODS/3NF
* **Status:** Approved
* **Context:** La capa de consumo requiere consultas analíticas rápidas con agregaciones complejas sobre ausentismo, salarios y rotación.
* **Decision:** Implementar un Esquema en Estrella (Star Schema) con 3 dimensiones y 3 tablas de hechos.
* **Consequences:** Simplifica la sintaxis de las medidas DAX en Power BI y optimiza el rendimiento de lectura eliminando uniones complejas en 3NF.

### ADR-003: Adoption of Python 3.11 for Ingestion, Data Prep & Quality Validation
* **Status:** Approved
* **Context:** El proyecto requiere un lenguaje flexible y unificado para generación sintética, validación de calidad de contratos e ingesta de datos.
* **Decision:** Adoptar Python 3.11 como lenguaje estándar de preparación de datos.
* **Consequences:** Simplifica el stack técnico, aprovecha el ecosistema de Pandas/SQLAlchemy y facilita la mantenibilidad del código.

### ADR-004: Selection of Power BI as Executive Visualization Platform
* **Status:** Approved
* **Context:** El C-Suite de MedTech Global Solutions utiliza el ecosistema Microsoft 365 para la toma de decisiones empresariales.
* **Decision:** Seleccionar Microsoft Power BI Pro/Premium para la capa de dashboards.
* **Consequences:** Adopción inmediata por parte de los ejecutivos, integración nativa con seguridad RLS y capacidades interactivas de simulación What-If.

### ADR-005: Implementation of Intermediate Analytical SQL Views for Workforce Dynamics
* **Status:** Approved
* **Context:** Se requiere calcular métricas agregadas complejas (Headcount mensual, Attrition rate acumulado, Bradford Factor) de forma precomputada para acelerar los dashboards de Power BI.
* **Decision:** Crear vistas analíticas intermedias optimizadas en PostgreSQL (`monthly_headcount_snapshot`, `monthly_attrition_summary`).
* **Consequences:** Desacopla la lógica pesada de agregación de la capa de visualización y garantiza consistencia absoluta de métricas.

### ADR-006: Implementation of Nightly Batch ELT Strategy over Real-Time Streaming
* **Status:** Approved
* **Context:** Los sistemas de RR. HH. y marcajes de tiempo no sufren variaciones críticas segundo a segundo que justifiquen infraestructura en tiempo real.
* **Decision:** Implementar un pipeline ELT procesado en lotes nocturnos (Nightly Batch a las 02:00 AM UTC).
* **Consequences:** Reduce drásticamente los costos de infraestructura, minimiza el impacto en los sistemas fuente en producción y simplifica el gobierno de datos.

### ADR-007: Implementation of Explainable Multi-Factor Risk Scoring for Retention Analytics
* **Status:** Approved
* **Context:** El CHRO y los HRBPs requieren un sistema explicable y accionable para priorizar retenciones de talento clave sin modelos opacos.
* **Decision:** Implementar un score multifactorial ponderado que evalúa la brecha salarial de mercado, sobretiempo acumulado y Factor de Bradford.
* **Consequences:** Otorga credibilidad total a las alertas del sistema, fundamentando la acción de los HRBPs con indicadores de negocio transparentes.

---

### 20.1 Architecture Design Sign-Off

```text
[✓] ARCHITECTURE DESIGN BASELINE APPROVED

Project Author: Emmanuel Rodríguez Mendoza
Professional Role: People Analytics / HR Data Analyst
Date: 2026-08-08
```
