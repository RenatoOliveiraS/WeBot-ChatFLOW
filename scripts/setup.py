#!/usr/bin/env python3
import os
import sys
import subprocess
import venv
import secrets
import shutil

def run(cmd, cwd=None):
    print(f"➡️  {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd)
    if res.returncode != 0:
        print(f"❌ Falha ao executar: {' '.join(cmd)}", file=sys.stderr)
        sys.exit(res.returncode)

def generate_env_file(example_path, target_path):
    """
    Copia .env.example → .env, gerando valores
    para chaves sensíveis (senha, secret_key) e
    mantendo os “nomes” fixos.
    """
    # defina aqui as chaves que devem ser geradas do zero
    gens = {
        'POSTGRES_PASSWORD': 16,   # 16 bytes → ~22 chars
        'REDIS_PASSWORD':      16,
        'SECRET_KEY':         32,   # 32 bytes → ~43 chars
    }

    with open(example_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out = []
    for line in lines:
        if line.strip().startswith('#') or '=' not in line:
            out.append(line)
            continue

        key, rest = line.split('=', 1)
        key = key.strip()
        if key in gens:
            token = secrets.token_urlsafe(gens[key])
            out.append(f"{key}={token}\n")
        else:
            # mantém exatamente como está no example
            out.append(line)

    with open(target_path, 'w', encoding='utf-8') as f:
        f.writelines(out)

    print(f"📝 `.env` criado em {target_path}")

def main():
    root = os.path.dirname(os.path.dirname(__file__))
    os.chdir(root)

    # 1) Virtualenv Python
    venv_dir = os.path.join(root, "venv")
    if not os.path.isdir(venv_dir):
        print("🔧 Criando virtualenv em ./venv")
        venv.create(venv_dir, with_pip=True)
    py = os.path.join(venv_dir, "Scripts" if os.name=='nt' else "bin", "python")

    # 2) Instala Python deps
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    run([py, "-m", "pip", "install", "-r", "backend/requirements.txt"])

    # 3) Instala dependências Node.js
    frontend = os.path.join(root, "frontend")
    # tenta achar 'npm' ou 'npm.cmd'
    npm_exe = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm_exe:
        print("❌ npm não encontrado. Instale o Node.js e verifique se o npm está no PATH.", file=sys.stderr)
        sys.exit(1)
    run([npm_exe, "install"], cwd=frontend)

    # 4) Gera .env se não existir
    example = os.path.join(root, ".env.example")
    target  = os.path.join(root, ".env")
    if not os.path.isfile(example):
        print(f"❌ Não encontrei `.env.example` em {example}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(target):
        print("🔐 Gerando `.env` com senhas e SECRET_KEY…")
        generate_env_file(example, target)
    else:
        print("ℹ️  `.env` já existe, pulando geração")

    # 5) Verifica variáveis obrigatórias
    run([py, os.path.join("scripts", "check_env.py")])

    # 6) Baixa imagens Docker
    print("🐳 Baixando imagens Docker necessárias…")

    # 6.1) Certifica-se de que o CLI do Docker existe
    docker_bin = shutil.which("docker")
    if not docker_bin:
        print("❌ Não encontrei o comando 'docker'. Instale o Docker Desktop e verifique se o 'docker' está no PATH.", file=sys.stderr)
        sys.exit(1)

    # 6.2) Testa se o engine está up
    info = subprocess.run([docker_bin, "info"], capture_output=True, text=True)
    if info.returncode != 0:
        print("❌ Não foi possível conectar ao Docker Engine. Verifique se o Docker Desktop ou o serviço Docker está em execução.", file=sys.stderr)
        # opcional: exibe erro original
        print(info.stderr, file=sys.stderr)
        sys.exit(1)

    # 6.3) Decide entre docker-compose vs docker compose
    compose_exe = shutil.which("docker-compose")
    if compose_exe:
        compose_cmd = [compose_exe]
    else:
        # fallback para 'docker compose'
        compose_cmd = [docker_bin, "compose"]

    # 6.4) Executa o pull
    res = subprocess.run(compose_cmd + ["pull"])
    if res.returncode != 0:
        print("⚠️ Alguns pulls falharam (imagens locais); indo para build…")

    # 2) Build dos serviços que têm build:
    res = subprocess.run(compose_cmd + ["build"])
    if res.returncode != 0:
        print(f"❌ Falha ao construir imagens locais.", file=sys.stderr)
        sys.exit(res.returncode)

    # compila serviços que precisam de build
    print("🏗️  Construindo serviços locais…")
    res = subprocess.run(compose_cmd + ["build"])
    if res.returncode != 0:
        print(f"❌ Falha ao construir: {' '.join(compose_cmd + ['build'])}", file=sys.stderr)
        sys.exit(res.returncode)

    print("✅ Docker pronto para uso.")

    print("✅ Setup concluído com sucesso.")

if __name__ == "__main__":
    main()
