# BUSINESS & TECHNICAL GLOSSARY
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & HR FINANCIAL OPTIMIZATION PLATFORM

**Document Version:** v0.5.0  
**Target Audience:** People Analytics Leaders, BI Managers, HR Business Partners, Technical Recruiters  
**Project Author:** Emmanuel Rodríguez Mendoza  
**Project:** Workforce Dynamic Lens  
**Date:** August 2026  
**Status:** Baseline Established (v0.5.0)  

---

## 1. Document Purpose

El **Business & Technical Glossary (`docs/Glossary.md`)** actúa como el diccionario de referencia unificado para la plataforma **Workforce Dynamic Lens**. 

Su objetivo principal es **eliminar la brecha conceptual** entre el dominio de Gestión Humana / People Analytics y la disciplina técnica de Análisis de Datos y Business Intelligence. Permite a reclutadores técnicos, líderes de RRHH y consultores analíticos comprender con precisión la terminología utilizada a lo largo de toda la suite documental (`docs/business_requirements.md`, `docs/data_dictionary.md`, `docs/KPIs_Definition.md`, `03_Architecture.md`, `04_Data_Model.md`).

---

## 2. People Analytics & Human Resources Domain

### Attrition (Rotación / Desvinculación Total)
* **Definición:** Número o porcentaje total de colaboradores que se desvinculan de la organización dentro de un periodo de tiempo determinado, abarcando salidas voluntarias e involuntarias.
* **Métrica Asociada:** `Tasa de Rotación General (%)`.
* **Impacto en Negocio:** Afecta directamente la estabilidad operativa y requiere inversión continua en reemplazo de personal.

### Voluntary Attrition (Rotación Voluntaria)
* **Definición:** Desvinculaciones iniciadas exclusivamente por decisión del colaborador (ej. renuncias por mejores ofertas del mercado, insatisfacción salarial o sobrecarga laboral).
* **Métrica Asociada:** `KPI-HR-01 (Voluntary Attrition Rate %)`.
* **Regla de Negocio:** `BR-02` (Excluye despidos con justa causa, jubilaciones o reestructuraciones).

### Regrettable Attrition (Rotación No Deseada / Fuga de Talento Clave)
* **Definición:** Desvinculación voluntaria de un colaborador clasificado como *High-Performer* (desempeño ≥ 4.0 / 5.0) o que ocupa una posición de difícil reemplazo (*Critical Position*).
* **Métrica Asociada:** `KPI-EXEC-01 (High-Performer Retention Rate %)`.
* **Impacto en Negocio:** Destruye el roadmap de producto en I+D, genera pérdida de propiedad intelectual y desacelera la entrega de proyectos.

### Bradford Score / Bradford Factor (Factor de Bradford)
* **Definición:** Indicador ponderado utilizado en operaciones para medir la severidad del ausentismo no programado de corta duración en una ventana de 12 meses.
* **Fórmula:**
```text
Bradford Factor Score (B) = S² × D
```
*Donde S es el número de instancias independientes de ausencia y D es el número total de días ausentes.*
* **Métrica Asociada:** `KPI-OP-01 (Bradford Factor Score)`.
* **Principio:** Penaliza con mayor severidad las ausencias cortas y frecuentes (ej. 10 ausencias de 1 día = 10² × 10 = 1,000 puntos) frente a ausencias largas continuas (ej. 1 ausencia de 10 días = 1² × 10 = 10 puntos).

### Compa-Ratio (Ratio de Competitividad Salarial)
* **Definición:** Proporción que evalúa la posición del salario base fijo de un colaborador individual respecto al punto medio de mercado (*Midpoint*) establecido para su puesto, nivel y país.
* **Fórmula:**
```text
Compa-Ratio = Salario Base Anual Fijado (USD) / Punto Medio de Mercado (Midpoint USD)
```
* **Métrica Asociada:** `KPI-HR-02 (Corporate Compa-Ratio)`.
* **Interpretación:** Un valor de 1.00 indica alineación exacta con la mediana del mercado. Valores < 0.85 señalan subpago significativo y alto riesgo de fuga.

### Flight Risk / Flight Risk Score (Riesgo de Rotación / Fuga)
* **Definición:** Score analítico multifactorial que pondera el nivel de riesgo de desvinculación voluntaria (Bajo, Medio, Alto) con base en variables objetivas de compensación, sobretiempo y ausentismo.
* **Métrica Asociada:** `KPI-PRED-01 (Individual Flight Risk Score)`.
* **Metodología:** Generado mediante consultas y vistas analíticas en SQL y medidas DAX en Power BI que evalúan el *Compa-Ratio*, la acumulación de horas extra en 30 días y el Factor de Bradford.

### Fully Loaded Cost (Costo Laboral Total Cargado)
* **Definición:** Costo económico total que representa un colaborador para la empresa. Incluye el salario base bruto fijado más un porcentaje adicional asignado a cargas prestacionales obligatorias, impuestos patronales y beneficios.
* **Regla de Negocio:** `BR-17` (Aplica un factor del 30% adicional sobre el salario base: `Salario Base Cargado = Salario Base × 1.30`).

### Headcount (Dotación / Plantilla Activa)
* **Definición:** Cantidad total de colaboradores contratados y activos en la fecha de corte analizada (`is_active = 1`).
* **Regla de Negocio:** `BR-01` (Excluye colaboradores con fecha de egreso efectiva anterior al corte).

### SLA Penalty / SLA Breach (Penalización por Acuerdos de Nivel de Servicio)
* **Definición:** Multa o cobro penal financiero aplicado por clientes corporativos B2B a la empresa debido a demoras o caídas en la cobertura de servicios de telemedicina.
* **Métrica Asociada:** `KPI-FIN-02 (SLA Penalty Attribution Cost $ USD)`.
* **Regla de Negocio:** `BR-15` (Costo paramétrico fijo de **$1,200 USD** por evento cuando la falla es atribuible a ausentismo operativo).

### Vacancy Cost (Costo de Vacancia)
* **Definición:** Pérdida financiera estimada por cada día que una posición estratégica permanece abierta sin cubrirse.
* **Regla de Negocio:** `BR-16` (Calculado como la cuota diaria del *Fully Loaded Cost* multiplicada por un factor de pérdida de productividad de **1.5x**).

---

## 3. Data Modeling, Analytics & BI Domain

### Data Contract (Contrato de Datos)
* **Definición:** Acuerdo técnico formal que especifica la estructura, reglas de calidad, tipos de datos, nulidad, linaje y políticas de privacidad que debe cumplir cualquier dataset de origen antes de ser consumido por el Data Warehouse o los modelos de analítica.
* **Documento del Proyecto:** `docs/data_dictionary.md` (v0.4.0).

### Data Lineage (Linaje de Datos)
* **Definición:** Mapeo completo del flujo de la información desde su sistema de origen transaccional (`Workday`, `Clock-In Logs`), pasando por las capas de ingesta, preparación y almacenamiento (`people_analytics`), hasta su uso en vistas analíticas de SQL y dashboards ejecutivos en Power BI.

### Dimension Table (Tabla de Dimensión)
* **Definición:** Tabla de un modelo relacional que almacena atributos descriptivos, contextuales y categóricos utilizados para filtrar, agrupar y segmentar métricas (ej. `dim_employees`, `dim_departments`, `dim_positions`).
* **Prefijo del Proyecto:** `dim_*`.

### ETL / ELT (Extract, Transform, Load / Extract, Load, Transform)
* **Definición:** Pipeline de ingeniería y preparación de datos encargado de extraer información de fuentes heterogéneas, transformarla (normalización, reglas de negocio, conversión de divisas) y cargarla en el Data Warehouse.
* **Implementación:** Scripts en Python 3.11+ utilizando `SQLAlchemy` y `Pandas` (`python/etl/`).

### Fact Table (Tabla de Hechos)
* **Definición:** Tabla central en un modelo dimensional que almacena transacciones numéricas, eventos contables y métricas cuantitativas observadas, acompañadas de claves foráneas (*Foreign Keys*) hacia las dimensiones (ej. `fact_attendance_logs`, `fact_terminations`, `fact_sla_events`).
* **Prefijo del Proyecto:** `fact_*`.

### KPI (Key Performance Indicator / Indicador Clave de Rendimiento)
* **Definición:** Métrica cuantitativa de alto nivel que mide directamente el grado de cumplimiento de un objetivo estratégico de negocio.
* **Documento del Proyecto:** `docs/KPIs_Definition.md` (v0.5.0).

### SCD Type 2 (Slowly Changing Dimension Type 2 / Dimensión de Variación Lenta Tipo 2)
* **Definición:** Técnica de modelado relacional que conserva el historial completo de cambios en atributos clave (ej. aumentos salariales o cambios de departamento). Cada modificación inserta una nueva fila en la tabla asignando fechas de vigencia (`row_effective_date`, `row_expiration_date`) y una bandera de fila actual (`is_current_row`).
* **Uso en el Proyecto:** Aplicado en `dim_employees` para auditar evoluciones salariales sin perder el estado histórico.

### Star Schema (Esquema en Estrella)
* **Definición:** Arquitectura de modelado dimensional (*Kimball*) compuesta por una o más tablas de hechos centrales rodeadas por tablas de dimensión desnormalizadas conectadas mediante uniones relacionales directas de 1:N.
* **Ventaja:** Maximiza la velocidad de lectura OLAP y simplifica el desarrollo de medidas DAX en Power BI.

---

## 4. Domain Terminology Mapping Matrix

| Concept / Term | Domain Focus | Technical Implementation | Primary Project Document |
| :--- | :--- | :--- | :--- |
| **Attrition / Turnover** | HR / People Analytics | SQL Aggregation & Views | `docs/business_requirements.md` |
| **Bradford Factor** | Operational Workforce Mgmt | SQL Window Functions & DAX | `docs/KPIs_Definition.md` |
| **Compa-Ratio** | Compensation & Total Rewards | SQL Join & DAX Measure | `docs/data_dictionary.md` |
| **Flight Risk Score** | People Analytics / Diagnostic | SQL Views & DAX Measures | `docs/KPIs_Definition.md` |
| **Star Schema** | Data Modeling / OLAP | PostgreSQL 16+ DDL | `04_Data_Model.md` |
| **Data Contract** | Data Governance | Validation Rules Engine | `docs/data_dictionary.md` |
| **SCD Type 2** | Database Engineering | Effective/Expiration Dates | `04_Data_Model.md` |