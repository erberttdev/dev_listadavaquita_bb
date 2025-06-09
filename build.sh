#!/bin/bash

echo "Iniciando o build..."

# instala dependências
pip install -r requirements.txt

# aplica as migrações

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build finalizado."

