@echo off

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Instala as dependências
pip install -r requirements.txt

REM Executa os testes
python scripts/run_tests.py 