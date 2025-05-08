#!/bin/bash

# Ativa o ambiente virtual
source venv/bin/activate

# Instala as dependências
pip install -r requirements.txt

# Executa os testes
python scripts/run_tests.py 