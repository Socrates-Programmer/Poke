# Entrypoint para inicializar la base de datos si es necesario
# Este script se puede usar en el contenedor de la base de datos

#!/bin/bash
set -e

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /app/init.sql
