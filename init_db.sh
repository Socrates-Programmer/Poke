# Entrypoint para inicializar la base de datos si es necesario
# Este script se puede usar en el contenedor de la base de datos

#!/bin/bash
set -e

mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < /app/init.sql
