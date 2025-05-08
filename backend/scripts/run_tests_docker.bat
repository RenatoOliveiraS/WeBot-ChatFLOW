@echo off

REM Executa os testes no container do backend
docker-compose exec backend python scripts/run_tests.py 