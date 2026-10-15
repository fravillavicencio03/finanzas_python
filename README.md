# 💰 Personal Finance Management System (CLI + SQLite)

Un sistema de gestión financiera personal diseñado para terminal de comandos (CLI) en Python 3, enfocado en el almacenamiento relacional seguro mediante **SQLite** y un diseño robusto de validación defensiva.

## 🚀 Características Principales

- **Base de Datos Relacional (SQL):** Almacenamiento persistente estructurado utilizando SQLite y sentencias parametrizadas seguras para prevenir inyecciones SQL.
- **Reportes Financieros Automáticos:** Cálculo en tiempo real de ingresos totales, gastos totales, balance neto (con indicadores de salud financiera) y desglose de gastos agrupados por categoría mediante funciones de agregación (`SUM`, `GROUP BY`).
- **CRUD Completo:** Permite registrar, listar, eliminar transacciones por ID y consultar resúmenes.
- **Validación Defensiva (Data Sanitization):** Filtros estrictos mediante `try/except` para impedir entradas negativas, textos vacíos en categorías, números en campos de texto y validación estricta de fechas con formato estándar ISO (`YYYY-MM-DD`) usando `datetime`.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Base de Datos:** SQLite3 (Nativa)
- **Librerías Nativas:** `datetime`, `sqlite3`
- **Herramientas:** Visual Studio Code, Git & GitHub

## 💻 Instrucciones de Ejecución

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/fravillavicencio03/finanzas_python.git](https://github.com/fravillavicencio03/finanzas_python.git)