import os
from cryptography.fernet import Fernet


# Garanta que a variável de ambiente FERNET_KEY aponte para a mesma chave usada
# pelo seu serviço (aquela de 32 bytes base64)
os.environ["FERNET_KEY"] = "sua-chave-base64-de-32-bytes"

# Sua senha real em texto puro
senha_plain = "LioN$012"

# Gera o token
token = encrypt_password(senha_plain)
print(token)  # copie essa saída: será algo como gAAAAABf...
