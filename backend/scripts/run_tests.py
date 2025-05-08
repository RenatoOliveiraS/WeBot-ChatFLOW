import os
import sys

import pytest


def main():
    """Executa os testes do projeto."""
    # Adiciona o diretório raiz ao PYTHONPATH
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)

    # Executa os testes
    args = [
        "app/tests",
        "-v",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html",
    ]
    return pytest.main(args)


if __name__ == "__main__":
    sys.exit(main())
