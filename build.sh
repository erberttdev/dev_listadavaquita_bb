#!/bin/bash

echo "Iniciando o build..."

# instala dependências
pip install -r requirements.txt

# aplica as migrações
python manage.py migrate

echo "Build finalizado."
