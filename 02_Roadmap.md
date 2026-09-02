# PROJECT ROADMAP & DEVELOPMENT PLAN
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & WORKFORCE DYNAMICS SOLUTION

**Document Version:** v0.9.0  
**Target Audience:** People Analytics Leaders, BI Managers, HR Business Partners, Data Analytics Recruiters  
**Project Author:** Emmanuel Rodríguez Mendoza  
**Professional Role:** People Analytics / HR Data Analyst  
**Project:** Workforce Dynamic Lens  
**Date:** August 2026  
**Status:** Fase 6 Completed (v0.9.0 Baseline) – In Progress (Fase 7: Portfolio Release & Showcase)  

---

## 1. Executive Overview

El **Project Roadmap & Development Plan (v0.9.0)** establece la planificación estratégica, las fases de desarrollo, los hitos de release por versión y el estado real de avance para la solución **Workforce Dynamic Lens**.

Este documento actúa como la guía de gestión del proyecto, definiendo el recorrido completo desde la formulación del problema de negocio en Recursos Humanos hasta la entrega de un portafolio profesional de nivel **People Analytics / HR Data Analyst**. Refleja con precisión el avance del repositorio, organizando el trabajo en **fases de desarrollo estructuradas** y manteniendo las versiones numéricas exclusivamente como **hitos de versión (*Release Milestones*)** alineados de forma estricta con el `CHANGELOG.md`.

---

## 2. Project Vision & Value Proposition

El objetivo de **Workforce Dynamic Lens** es servir como un proyecto de portafolio que demuestre la integración fluida entre el **conocimiento estratégico del dominio de Recursos Humanos** y la **analítica aplicada de datos**.

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PROJECT VISION & VALUE PROPOSITION                                                              │
│ (Perfil: People Analytics / HR Data Analyst)                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  Conocimiento del Dominio de RR. HH. y Psicología Organizacional                                │
│         │                                                                                       │
│         ├─► Formulación del Problema & Monetización Financiera (Impacto en P&L, Vacantes, Ausentismo)│
│         │                                                                                       │
│  Ejecución Analítica, Modelado Dimensional & Business Intelligence                              │
│         │                                                                                       │
│         ├─► Modelado Dimensional & Catálogo de Métricas (Modelo Estrella, Diccionario de Datos, KPIs HR)│
│         ├─► Preparación & Carga de Datos (PostgreSQL local, Scripts SQL DDL, Generación Sintética & ETL Python)│
│         ├─► Análisis Exploratorio & Factores de Riesgo (Diagnóstico de Rotación, Ausentismo y Compa-Ratio)│
│         └─► Dashboards Ejecutivos & Storytelling (Power BI Interactivo, Medidas DAX & Simulador What-If)│
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Development Phases (Fases de Desarrollo)

El desarrollo del proyecto se estructura en **7 fases secuenciales**, garantizando una progresión lógica donde cada fase fundamenta a la siguiente:

```text
[ Fase 1: Business Understanding ] ──► [ Fase 2: Analytics Design ] ──► [ Fase 3: Data Prep & Ingestion ]
                                                                                   │
[ Fase 7: Portfolio Showcase (In Progress) ] ◄─ [ Fase 6: QA & Testing (Completed) ] ◄─ [ Fase 5: Power BI ] ◄─ [ Fase 4: Workforce Analytics ]
```

### Fase 1: Business Understanding & HR Strategy
* **Estado:** Completed
* **Hitos de Versión:** `v0.1.0` – `v0.3.0`
* **Objetivo:** Definir el problema de negocio, cuantificar las pérdidas en P&L por rotación voluntaria y ausentismo, y establecer las preguntas de negocio y requerimientos funcionales.
* **Entregables:** `01_Project_Charter.md`, `Company_Profile.md`, `Business_Case.md`, `business_requirements.md`.

### Fase 2: Analytics, Data & Architecture Design
* **Estado:** Completed
* **Hitos de Versión:** `v0.4.0` – `v0.5.0`
* **Objetivo:** Estructurar el diccionario de datos, definir el catálogo de KPIs de People Analytics, diseñar la arquitectura técnica y establecer el modelo dimensional en estrella (Kimball).
* **Entregables:** `data_dictionary.md`, `KPIs_Definition.md`, `03_Architecture.md`, `04_Data_Model.md`, `02_Roadmap.md`, `05_Tasks.md`.

### Fase 3: Data Preparation, Ingestion & Quality Validation
* **Estado:** Completed
* **Hito de Versión:** `v0.6.0`
* **Objetivo:** Inicializar la base de datos PostgreSQL, construir las tablas y esquema `people_analytics`, desarrollar el generador de datos sintéticos en Python y ejecutar el pipeline ETL con validación de calidad.
* **Entregables:** Base de datos PostgreSQL `workforce_db`, scripts DDL `sql/schema/`, generador sintético `python/data_generation/`, pipeline ETL `python/etl/`.

### Fase 4: Exploratory Workforce Analysis & Diagnostic Analytics
* **Estado:** Completed
* **Hito de Versión:** `v0.7.0`
* **Objetivo:** Realizar el análisis exploratorio de datos (EDA) multivariado, construir vistas analíticas en SQL, reconciliar consistencia de empleados terminados y calcular factores de riesgo de salida y patrones de ausentismo.
* **Entregables:** Notebooks `notebooks/`, vistas maestras `sql/analytics/13_views.sql`, suite de validación `sql/analytics/14_validation_queries.sql`, reconciliación SCD2.

### Fase 5: Business Intelligence Suite & Executive Storytelling
* **Estado:** Completed
* **Hito de Versión:** `v0.8.0`
* **Objetivo:** Desarrollar el modelo semántico en Power BI, construir medidas DAX estructuradas por carpetas de exhibición, diseñar 3 tableros ejecutivos interactivos (Visión General de RR. HH., Diagnóstico de Ausentismo y Riesgo de Rotación) e implementar simulador financiero *What-If*.
* **Entregables:** Archivo `.pbix` en `powerbi/`, documento `docs/Business_Insights.md`, deck ejecutivo de presentación (`presentations/Executive_Presentation.pptx`).

### Fase 6: Quality Assurance, Testing & Performance Optimization
* **Estado:** Completed
* **Hito de Versión:** `v0.9.0`
* **Objetivo:** Refactorizar código en Python y SQL, realizar pruebas integrales de extremo a extremo, optimizar índices y medidas DAX, y auditar la trazabilidad documental.
* **Entregables:** Código refactorizado (PEP8/SQL standard), informe de calidad de datos y auditoría de consistencia de métricas.

### Fase 7: Portfolio Release & Showcase
* **Estado:** In Progress
* **Hito de Versión:** `v1.0.0`
* **Objetivo:** Redactar el `README.md` ejecutivo principal, capturar assets visuales de alta calidad, preparar el caso de estudio para entrevistas y publicar el release v1.0.0 en GitHub.
* **Entregables:** `README.md` de portafolio final, capturas/GIFs de dashboards, caso de estudio preparado, Git Tag `v1.0.0`.

---

## 4. Release Milestones (Hitos de Release por Versión)

Las versiones numéricas del proyecto representan **hitos de entrega (*Release Milestones*)** y están alineadas estrictamente con el registro de cambios (`CHANGELOG.md`):

| Versión | Hito / Enfoque | Fase Asociada | Estado |
| :--- | :--- | :--- | :--- |
| **v0.1.0** | Project Setup & Repository Initialization | Fase 1 | Completed |
| **v0.2.0** | Business Charter & Company Profile Baseline | Fase 1 | Completed |
| **v0.3.0** | Business Case & Functional Requirements Baseline | Fase 1 | Completed |
| **v0.4.0** | Data Dictionary & Data Specifications Baseline | Fase 2 | Completed |
| **v0.5.0** | Analytics Design, Data Model, Architecture & Roadmap | Fase 2 | Completed |
| **v0.6.0** | Synthetic Data Generator, PostgreSQL DB & ETL Pipeline | Fase 3 | Completed |
| **v0.7.0** | Exploratory Data Analysis, SQL Views & System Reconciliation | Fase 4 | Completed |
| **v0.8.0** | Power BI Executive Dashboards Suite, DAX & Business Insights Report | Fase 5 | Completed |
| **v0.9.0** | Quality Assurance, Testing, Code Refactoring & Performance | Fase 6 | Completed |
| **v1.0.0** | Production Portfolio Release, README Storytelling & GitHub Showcase | Fase 7 | In Progress |

---

## 5. Current Progress Tracking

El avance del proyecto se evalúa de manera objetiva según el estado de ejecución de cada fase de desarrollo:

| Fase de Desarrollo | Rango de Versiones | Estado | Entregables Clave |
| :--- | :--- | :--- | :--- |
| **Fase 1: Business Understanding** | v0.1.0 – v0.3.0 | **Completed** | Charter, Company Profile, Business Case, BRS |
| **Fase 2: Analytics & Data Design** | v0.4.0 – v0.5.0 | **Completed** | Data Dictionary, KPIs, Architecture, Data Model, Roadmap, Tasks |
| **Fase 3: Data Prep & Ingestion** | v0.6.0 | **Completed** | PostgreSQL DB, DDL SQL, Generador Sintético Python, Pipeline ETL |
| **Fase 4: Workforce Analytics & SQL**| v0.7.0 | **Completed** | Notebooks EDA, Vistas SQL, Reconciliación SCD2, Queries de Validación |
| **Fase 5: Business Intelligence Suite** | v0.8.0 | **Completed** | Archivo `.pbix` Power BI, Medidas DAX, Reporte de Insights |
| **Fase 6: QA, Testing & Optimization** | v0.9.0 | **Completed** | Código refactorizado, Pruebas E2E, Índices SQL, Auditoría |
| **Fase 7: Portfolio Release & Showcase** | v1.0.0 | **In Progress** | README Ejecutivo Final, Assets de Portafolio, Caso de Estudio |

---

## 6. Major Project Milestones

| ID | Descripción del Hito | Fase | Versión | Estado |
| :--- | :--- | :--- | :--- | :--- |
| **MS-01** | Formulación del problema de negocio e impacto financiero en P&L | Fase 1 | v0.2.0 | Completed |
| **MS-02** | Especificación de Requerimientos Funcionales y Reglas de Negocio | Fase 1 | v0.3.0 | Completed |
| **MS-03** | Estructuración del Diccionario de Datos y Catálogo de KPIs | Fase 2 | v0.4.0 | Completed |
| **MS-04** | Diseño del Modelo Dimensional (Esquema Estrella) y Arquitectura Analítica | Fase 2 | v0.5.0 | Completed |
| **MS-05** | Definición del Roadmap de Proyecto y Registro de Tareas | Fase 2 | v0.5.0 | Completed |
| **MS-06** | Inicialización de PostgreSQL, Generación Sintética y Pipeline ETL | Fase 3 | v0.6.0 | Completed |
| **MS-07** | Vistas Analíticas en SQL, Reconciliación SCD2 y Análisis Exploratorio de Talento | Fase 4 | v0.7.0 | Completed |
| **MS-08** | Desarrollo de Tableros en Power BI, Medidas DAX e Informe de Insights | Fase 5 | v0.8.0 | Completed |
| **MS-09** | Refactorización de Código, Pruebas E2E y Auditoría de Consistencia | Fase 6 | v0.9.0 | Completed |
| **MS-10** | Publicación Final del Repositorio de Portafolio en GitHub | Fase 7 | v1.0.0 | In Progress |

---

## 7. Future Enhancements (Post-v1.0.0 Scope)

Funcionalidades de valor analítico identificadas para futuras iteraciones del portafolio, orientadas a profundizar el análisis en People Analytics:

1. **Análisis de Supervivencia Kaplan-Meier:** Implementación de curvas de retención en Python para estimar la vida útil laboral esperada (*tenure expected*) según el departamento y rol.
2. **Análisis Cualitativo de Encuestas de Exit Interview:** Procesamiento de texto básico sobre comentarios cualitativos en entrevistas de salida y encuestas de clima.
3. **Escenarios Avanzados de Simulación de Compensación:** Expansión del simulador de impacto financiero en Power BI para modelar bandas salariales por mercado regional.

---

## 8. Key Risks & Mitigation Strategy

| Descripción del Riesgo | Impacto | Probabilidad | Estrategia de Mitigación |
| :--- | :--- | :--- | :--- |
| **Falta de realismo en datos sintéticos** | Alto | Media | Diseñar en Python distribuciones estadísticas con correlaciones lógicas de RR. HH. (ej. mayor brecha salarial → mayor rotación). |
| **Rendimiento deficiente en DAX** | Medio | Baja | Garantizar un esquema en estrella estricto (1:N) con relaciones de una sola dirección y preconsolidar agregaciones pesadas en SQL. |
| **Inconsistencias en granularidad temporal** | Alto | Baja | Extensión formal de `dim_date` y sincronización estricta de fechas de alta y egreso. |
| **Inconsistencia entre documentos** | Alto | Baja | Mantener matrices de trazabilidad explícitas entre preguntas de negocio, KPIs, modelo de datos y dashboards. |

---

## 9. Portfolio Success Criteria (Definition of Done)

El proyecto se considerará completo y listo para demostración en procesos de selección de **People Analytics / HR Data Analyst** cuando cumpla con los siguientes criterios:

1. **Suite Documental Coherente:** Documentación profesional en Markdown que conecte la visión de negocio con el diseño técnico.
2. **Base de Datos y Script ETL Funcionales:** Base de datos PostgreSQL estructurada y script reproducible en Python para generar datos e ingestar el esquema estrella.
3. **Vistas SQL y Métricas Analíticas Auditadas:** Conjunto de vistas SQL y consultas de validación con 0 violaciones de integridad referencial.
4. **Dashboards Ejecutivos en Power BI:** Archivo `.pbix` interactivo con reporte de rotación, ausentismo e impacto financiero, construido sobre medidas DAX optimizadas.
5. **Storytelling & README de Alto Nivel:** `README.md` estructurado que comunique el impacto en el negocio y demuestre capacidades end-to-end de análisis de datos en RR. HH.