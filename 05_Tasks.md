# PROJECT TASKS & DEVELOPMENT BACKLOG
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & WORKFORCE DYNAMICS SOLUTION

**Document Version:** v1.0.0  
**Project Author:** Emmanuel Rodríguez Mendoza  
**Professional Role:** People Analytics / HR Data Analyst  
**Project:** Workforce Dynamic Lens  
**Date:** 2026-09-02  
**Status:** 100% Completed – v1.0.0 Production Release Published & Tagged  

---

## 1. Executive Backlog Summary

| Task ID | Version | Phase | Task Description | Priority | Depends On | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TSK-101** | v0.1.0 | Business Understanding | Repository Initialization & Directory Setup | High | None | Completed |
| **TSK-102** | v0.2.0 | Business Understanding | Project Charter Definition (`01_Project_Charter.md`) | High | TSK-101 | Completed |
| **TSK-103** | v0.2.0 | Business Understanding | Company Profile (`Company_Profile.md`) | Medium | TSK-101 | Completed |
| **TSK-104** | v0.3.0 | Business Understanding | Business Case & Financial P&L (`Business_Case.md`) | High | TSK-102 | Completed |
| **TSK-105** | v0.3.0 | Business Understanding | Business Requirements Specification (`business_requirements.md`) | High | TSK-104 | Completed |
| **TSK-201** | v0.4.0 | Analytics & Data Design | Data Dictionary & Data Contract (`data_dictionary.md`) | High | TSK-105 | Completed |
| **TSK-202** | v0.5.0 | Analytics & Data Design | KPIs & HR Metrics Catalog (`KPIs_Definition.md`) | High | TSK-201 | Completed |
| **TSK-203** | v0.5.0 | Analytics & Data Design | Analytics Platform Architecture (`03_Architecture.md`) | High | TSK-201 | Completed |
| **TSK-204** | v0.5.0 | Analytics & Data Design | Star Schema Dimensional Model (`04_Data_Model.md`) | High | TSK-201 | Completed |
| **TSK-205** | v0.5.0 | Analytics & Data Design | Project Roadmap & Release Plan (`02_Roadmap.md`) | Medium | TSK-203 | Completed |
| **TSK-206** | v0.5.0 | Analytics & Data Design | Project Tasks & Backlog Definition (`05_Tasks.md`) | Medium | TSK-205 | Completed |
| **TSK-300** | v0.6.0 | Data Prep & Ingestion | PostgreSQL Database & Schema Initialization | High | TSK-204 | Completed |
| **TSK-301** | v0.6.0 | Data Prep & Ingestion | DDL SQL Scripts & Schema Constraints (`sql/schema/`) | High | TSK-300 | Completed |
| **TSK-302** | v0.6.0 | Data Prep & Ingestion | Python Synthetic Data Generator Engine | High | TSK-301 | Completed |
| **TSK-303** | v0.6.0 | Data Prep & Ingestion | ETL Pipeline & PostgreSQL Ingestion Script | High | TSK-302 | Completed |
| **TSK-304** | v0.6.0 | Data Prep & Ingestion | Data Quality Validation & Automated Checks | Medium | TSK-303 | Completed |
| **TSK-401** | v0.7.0 | Workforce Analytics & SQL | Exploratory Data Analysis (EDA) & SQL Views | Medium | TSK-303 | Completed |
| **TSK-402** | v0.7.0 | Workforce Analytics & SQL | SCD2 Reconciliation & Historical Tracking Maintenance | High | TSK-401 | Completed |
| **TSK-403** | v0.7.0 | Workforce Analytics & SQL | Attrition Multivariate Diagnostics & Risk Scoring Logic | High | TSK-402 | Completed |
| **TSK-404** | v0.7.0 | Workforce Analytics & SQL | Compa-Ratio, Bradford & Overtime Multi-Factor Synthesis | High | TSK-403 | Completed |
| **TSK-501** | v0.8.0 | Business Intelligence Suite | Power BI Dimensional Model & DAX Measures Group | High | TSK-303 | Completed |
| **TSK-502** | v0.8.0 | Business Intelligence Suite | Executive Dashboards Design (3 Interactive Screens) | High | TSK-501 | Completed |
| **TSK-503** | v0.8.0 | Business Intelligence Suite | Business Insights Report & Executive Storytelling | High | TSK-502 | Completed |
| **TSK-601** | v0.9.0 | QA, Testing & Optimization | Code Refactoring (PEP8 & SQL Standards) | Medium | TSK-403, TSK-501 | Completed |
| **TSK-602** | v0.9.0 | QA, Testing & Optimization | End-to-End Pipeline Testing & Metric Validation | High | TSK-303, TSK-403 | Completed |
| **TSK-603** | v0.9.0 | QA, Testing & Optimization | Performance Optimization (Indexes & DAX) | Medium | TSK-301, TSK-501 | Completed |
| **TSK-604** | v0.9.0 | QA, Testing & Optimization | Documentation Audit & Traceability Review | High | TSK-201, TSK-503 | Completed |
| **TSK-701** | v1.0.0 | Portfolio Release & Showcase | Final Executive README & Storytelling | High | TSK-604 | Completed |
| **TSK-702** | v1.0.0 | Portfolio Release & Showcase | Portfolio Assets (Screenshots, Demo GIFs) | Medium | TSK-502 | Completed |
| **TSK-703** | v1.0.0 | Portfolio Release & Showcase | Interview Case Study & Candidate Guide (STAR) | Medium | TSK-701 | Completed |
| **TSK-704** | v1.0.0 | Portfolio Release & Showcase | GitHub Public Repository Release (v1.0.0) | High | TSK-701 | Completed |

---

## 2. Detailed Task Breakdown by Release Milestone

### Release Milestone v0.1.0 – v0.3.0: Business Understanding & HR Strategy
* **Fase de Desarrollo:** Fase 1: Business Understanding
* **Estado del Release:** Completed

- [x] **TSK-101:** Repository Initialization & Setup
  * **Versión:** v0.1.0 | **Prioridad:** High | **Dependencias:** Ninguna | **Estado:** Completed
  * **Descripción:** Configurar estructura base de carpetas, licencias, `.gitignore`, `CHANGELOG.md` e inicializar repositorio Git.
- [x] **TSK-102:** Project Charter Definition
  * **Versión:** v0.2.0 | **Prioridad:** High | **Dependencias:** TSK-101 | **Estado:** Completed
  * **Descripción:** Elaborar `01_Project_Charter.md` especificando objetivos del proyecto, alcance de People Analytics y gobernanza.
- [x] **TSK-103:** Company Profile Definition
  * **Versión:** v0.2.0 | **Prioridad:** Medium | **Dependencias:** TSK-101 | **Estado:** Completed
  * **Descripción:** Definir `Company_Profile.md` detallando el perfil organizacional de MedTech Global Solutions (4.500 empleados, departamentos y roles).
- [x] **TSK-104:** Business Case & Financial Impact
  * **Versión:** v0.3.0 | **Prioridad:** High | **Dependencias:** TSK-102 | **Estado:** Completed
  * **Descripción:** Crear `Business_Case.md` monetizando el impacto financiero de la rotación voluntaria y el ausentismo laboral en P&L.
- [x] **TSK-105:** Business Requirements Specification (BRS)
  * **Versión:** v0.3.0 | **Prioridad:** High | **Dependencias:** TSK-104 | **Estado:** Completed
  * **Descripción:** Desarrollar `business_requirements.md` especificando 31 preguntas de negocio, 42 requerimientos funcionales y 32 reglas de negocio con matriz de trazabilidad.

---

### Release Milestone v0.4.0 – v0.5.0: Analytics, Data & Architecture Design
* **Fase de Desarrollo:** Fase 2: Analytics & Data Design
* **Estado del Release:** Completed

- [x] **TSK-201:** Data Dictionary & Contract Specification
  * **Versión:** v0.4.0 | **Prioridad:** High | **Dependencias:** TSK-105 | **Estado:** Completed
  * **Descripción:** Elaborar `data_dictionary.md` estructurando metadatos de 7 entidades analíticas, llaves, tipos de datos y clasificaciones GDPR/PII.
- [x] **TSK-202:** KPIs & HR Metrics Catalog Definition
  * **Versión:** v0.5.0 | **Prioridad:** High | **Dependencias:** TSK-201 | **Estado:** Completed
  * **Descripción:** Definir `KPIs_Definition.md` con fórmulas estandarizadas, grano analítico y categorización de métricas de RR. HH.
- [x] **TSK-203:** Analytics Platform Architecture Specification
  * **Versión:** v0.5.0 | **Prioridad:** High | **Dependencias:** TSK-201 | **Estado:** Completed
  * **Descripción:** Diseñar `03_Architecture.md` estableciendo el flujo analítico end-to-end (PostgreSQL → Python → Power BI).
- [x] **TSK-204:** Star Schema Dimensional Data Model
  * **Versión:** v0.5.0 | **Prioridad:** High | **Dependencias:** TSK-201 | **Estado:** Completed
  * **Descripción:** Construir `04_Data_Model.md` detallando el esquema estrella Kimball (`dim_employees`, `dim_departments`, `fact_attendance_logs`, etc.).
- [x] **TSK-205:** Project Roadmap & Release Plan
  * **Versión:** v0.5.0 | **Prioridad:** Medium | **Dependencias:** TSK-203 | **Estado:** Completed
  * **Descripción:** Actualizar `02_Roadmap.md` organizando las fases de desarrollo y manteniendo versiones numéricas como hitos de release.
- [x] **TSK-206:** Project Tasks & Backlog Definition
  * **Versión:** v0.5.0 | **Prioridad:** Medium | **Dependencias:** TSK-205 | **Estado:** Completed
  * **Descripción:** Consolidar `05_Tasks.md` definiendo el backlog oficial de tareas con resumen matricial, prioridades y dependencias.

---

### Release Milestone v0.6.0: Data Preparation, Ingestion & Quality Validation
* **Fase de Desarrollo:** Fase 3: Data Prep & Ingestion
* **Estado del Release:** Completed

- [x] **TSK-300:** PostgreSQL Database & Schema Initialization
  * **Versión:** v0.6.0 | **Prioridad:** High | **Dependencias:** TSK-204 | **Estado:** Completed
  * **Descripción:** Crear la base de datos `workforce_db` e inicializar el esquema relacional `people_analytics` en PostgreSQL.
- [x] **TSK-301:** DDL SQL Scripts & Schema Constraints
  * **Versión:** v0.6.0 | **Prioridad:** High | **Dependencias:** TSK-300 | **Estado:** Completed
  * **Descripción:** Escribir scripts SQL DDL (`sql/schema/`) definiendo tablas, llaves primarias/foráneas e índices analíticos.
- [x] **TSK-302:** Python Synthetic Data Generator Engine
  * **Versión:** v0.6.0 | **Prioridad:** High | **Dependencias:** TSK-301 | **Estado:** Completed
  * **Descripción:** Desarrollar motor en Python (`python/data_generation/`) incorporando distribuciones estadísticas y dinámicas de RR. HH. realistas.
- [x] **TSK-303:** ETL Pipeline & PostgreSQL Ingestion Script
  * **Versión:** v0.6.0 | **Prioridad:** High | **Dependencias:** TSK-302 | **Estado:** Completed
  * **Descripción:** Construir el script ETL reproducible (`python/etl/`) para transformación, limpieza e ingesta a PostgreSQL.
- [x] **TSK-304:** Data Quality Validation & Automated Checks
  * **Versión:** v0.6.0 | **Prioridad:** Medium | **Dependencias:** TSK-303 | **Estado:** Completed
  * **Descripción:** Implementar validaciones automáticas de integridad referencial, nulos y rangos permitidos antes del consumo analítico.

---

### Release Milestone v0.7.0: Exploratory Workforce Analysis & SQL Diagnostic Views
* **Fase de Desarrollo:** Fase 4: Workforce Analytics & SQL
* **Estado del Release:** Completed

- [x] **TSK-401:** Exploratory Data Analysis (EDA) & SQL Views
  * **Versión:** v0.7.0 | **Prioridad:** Medium | **Dependencias:** TSK-303 | **Estado:** Completed
  * **Descripción:** Construcción de vistas maestras en SQL (`sql/analytics/13_views.sql`) identificando patrones de rotación, ausentismo y compa-ratio.
- [x] **TSK-402:** SCD2 Reconciliation & Historical Tracking Maintenance
  * **Versión:** v0.7.0 | **Prioridad:** High | **Dependencias:** TSK-401 | **Estado:** Completed
  * **Descripción:** Reconciliación formal SCD2 entre bajas y empleados activos, eliminando registros inconsistentes de asistencia y auditando consistencia.
- [x] **TSK-403:** Attrition Multivariate Diagnostics & Risk Scoring Logic
  * **Versión:** v0.7.0 | **Prioridad:** High | **Dependencias:** TSK-402 | **Estado:** Completed
  * **Descripción:** Modelado analítico y diagnóstico multivariado de factores de riesgo de rotación voluntaria en roles clave.
- [x] **TSK-404:** Compa-Ratio, Bradford & Overtime Multi-Factor Synthesis
  * **Versión:** v0.7.0 | **Prioridad:** High | **Dependencias:** TSK-403 | **Estado:** Completed
  * **Descripción:** Integración analítica y ponderación de variables de talento (Compa-Ratio, horas extra, Bradford Score) en score de riesgo de retención.

---

### Release Milestone v0.8.0: Business Intelligence Suite & Executive Storytelling
* **Fase de Desarrollo:** Fase 5: Business Intelligence Suite
* **Estado del Release:** Completed

- [x] **TSK-501:** Power BI Dimensional Model & DAX Measures Group
  * **Versión:** v0.8.0 | **Prioridad:** High | **Dependencias:** TSK-303 | **Estado:** Completed
  * **Descripción:** Construir modelo semántico en Power BI Desktop (`powerbi/People_Analytics_Executive_Suite_MedTech.pbix`) e implementar grupo de medidas DAX avanzadas.
- [x] **TSK-502:** Executive Dashboards Design (3 Interactive Screens)
  * **Versión:** v0.8.0 | **Prioridad:** High | **Dependencias:** TSK-501 | **Estado:** Completed
  * **Descripción:** Diseñar 3 tableros ejecutivos interactivos (Visión General de RR. HH., Diagnóstico de Ausentismo y Riesgo de Rotación con Simulador What-If).
- [x] **TSK-503:** Business Insights Report & Executive Storytelling
  * **Versión:** v0.8.0 | **Prioridad:** High | **Dependencias:** TSK-502 | **Estado:** Completed
  * **Descripción:** Redactar informe de hallazgos ejecutivos (`docs/Business_Insights.md`) estableciendo la verdad oficial de las cifras ($6.44M P&L, focos rojos y ROI).

---

### Release Milestone v0.9.0: Quality Assurance, Testing & Optimization
* **Fase de Desarrollo:** Fase 6: QA, Testing & Optimization
* **Estado del Release:** Completed

- [x] **TSK-601:** Code Refactoring (PEP8 & SQL Standards)
  * **Versión:** v0.9.0 | **Prioridad:** Medium | **Dependencias:** TSK-403, TSK-501 | **Estado:** Completed
  * **Descripción:** Refactorizar scripts en Python y consultas SQL asegurando estándares de legibilidad, modularidad y estilo.
- [x] **TSK-602:** End-to-End Pipeline Testing & Metric Validation
  * **Versión:** v0.9.0 | **Prioridad:** High | **Dependencias:** TSK-303, TSK-403 | **Estado:** Completed
  * **Descripción:** Ejecutar pruebas integrales de extremo a extremo validando que la ingesta, vistas analíticas y medidas DAX en dashboards se sincronicen al 100%.
- [x] **TSK-603:** Performance Optimization (Indexes & DAX)
  * **Versión:** v0.9.0 | **Prioridad:** Medium | **Dependencias:** TSK-301, TSK-501 | **Estado:** Completed
  * **Descripción:** Optimizar índices en PostgreSQL y ajustar fórmulas DAX en Power BI para garantizar tiempos de respuesta fluidos.
- [x] **TSK-604:** Documentation Audit & Traceability Review
  * **Versión:** v0.9.0 | **Prioridad:** High | **Dependencias:** TSK-201, TSK-503 | **Estado:** Completed
  * **Descripción:** Auditar la consistencia y trazabilidad entre requerimientos de negocio, métricas, código, base de datos y reportes.

---

### Release Milestone v1.0.0: Production Portfolio Release & Showcase
* **Fase de Desarrollo:** Fase 7: Portfolio Release & Showcase
* **Estado del Release:** Completed

- [x] **TSK-701:** Final Executive README & Storytelling
  * **Versión:** v1.0.0 | **Prioridad:** High | **Dependencias:** TSK-604 | **Estado:** Completed
  * **Descripción:** Redactar el `README.md` principal estructurado como un reporte ejecutivo enfocado en valor de negocio y competencias técnicas.
- [x] **TSK-702:** Portfolio Assets (Screenshots & Demo GIFs)
  * **Versión:** v1.0.0 | **Prioridad:** Medium | **Dependencias:** TSK-502 | **Estado:** Completed
  * **Descripción:** Capturar e integrar imágenes de alta resolución y demostraciones animadas de los dashboards de Power BI.
- [x] **TSK-703:** Interview Case Study & Candidate Guide (STAR)
  * **Versión:** v1.0.0 | **Prioridad:** Medium | **Dependencias:** TSK-701 | **Estado:** Completed
  * **Descripción:** Preparar guía de presentación de caso de estudio para entrevistas de People Analytics / HR Data Analyst estructurada en método STAR.
- [x] **TSK-704:** GitHub Public Repository Release (v1.0.0)
  * **Versión:** v1.0.0 | **Prioridad:** High | **Dependencias:** TSK-701 | **Estado:** Completed
  * **Descripción:** Publicar oficialmente el release v1.0.0 en GitHub con etiquetado de versión (*Git Tag*) y documentación finalizada.
