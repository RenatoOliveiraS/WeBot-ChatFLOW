#!/usr/bin/env python3
import os
import sys

from dotenv import dotenv_values, load_dotenv


def main():
    here = os.path.dirname(__file__)
    env_path = os.path.join(here, "..", ".env")
    example_path = os.path.join(here, "..", ".env.example")

    # 0) Falha se não houver .env
    if not os.path.isfile(env_path):
        prefix = "Erro: arquivo(.env) de variáveis de "
        suffix = "ambiente não encontrado na raiz do projeto"
        print(prefix, suffix)
        sys.exit(1)

    # 1) Carrega .env sobrescrevendo tudo
    load_dotenv(env_path, override=True)

    # 2) Falha se não houver .env.example
    if not os.path.isfile(example_path):
        print(f"Erro: não encontrei o arquivo {example_path}", file=sys.stderr)
        sys.exit(1)

    # 3) Extrai chaves do .env.example
    config = dotenv_values(example_path)
    keys = [k for k in config.keys() if k]

    # 4) Verifica se estão definidas e não vazias
    missing = []
    for k in keys:
        v = os.getenv(k)
        if v is None or v.strip() == "":
            missing.append(k)

    if missing:
        msg = "❌ Variáveis de ambiente ausentes ou sem valor: " + ", ".join(missing)
        print(msg, file=sys.stderr)
        sys.exit(1)

    print("✅ Todas as variáveis de ambiente estão definidas e preenchidas.")
    sys.exit(0)


if __name__ == "__main__":
    main()
