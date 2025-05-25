# src/features/email_connections/service.py

import os
import smtplib
import imaplib
import socket
from cryptography.fernet import Fernet, InvalidToken
from sqlmodel import Session


from .model import EmailConnection
from src.features.inbound_emails.service import ingest_raw_email  # ajusta o import conforme seu projeto

# Carrega a chave do .env
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise RuntimeError("A variável de ambiente FERNET_KEY não está definida")

try:
    fernet = Fernet(FERNET_KEY.encode())
except (ValueError, TypeError) as e:
    raise RuntimeError("FERNET_KEY inválida: deve ser base64 de 32 bytes") from e


def encrypt_password(plain: str) -> str:
    """
    Encripta a senha em texto plano retornando uma string em base64.
    """
    return fernet.encrypt(plain.encode()).decode()


def decrypt_password(encrypted: str) -> str:
    """
    Decripta a senha (base64) de volta ao texto original.
    """
    try:
        return fernet.decrypt(encrypted.encode()).decode()
    except InvalidToken as e:
        raise RuntimeError(
            "Falha ao descriptografar a senha: token inválido ou chave incorreta"
        ) from e


def test_email_connection(connection: EmailConnection) -> None:
    """
    Tenta estabelecer uma conexão SMTP com as configurações fornecidas.
    Pode lançar:
      - RuntimeError (ao descriptografar a senha)
      - smtplib.SMTPException (falha SMTP)
      - socket.timeout (timeout de rede)
    """
    password = decrypt_password(connection.password_encrypted)

    if connection.use_ssl:
        server = smtplib.SMTP_SSL(
            connection.smtp_server,
            connection.smtp_port,
            timeout=10
        )
    else:
        server = smtplib.SMTP(
            connection.smtp_server,
            connection.smtp_port,
            timeout=10
        )

    try:
        if connection.use_tls and not connection.use_ssl:
            server.starttls()
        server.login(connection.username, password)
    finally:
        server.quit()


def fetch_inbound_emails(connection: EmailConnection, db: Session) -> int:
    """
    Conecta via IMAP, busca mensagens UNSEEN em `imap_folder`,
    persiste usando ingest_raw_email e marca como SEEN.
    Retorna o número de e-mails processados.
    """
    pwd = decrypt_password(connection.password_encrypted)

    # escolhe classe IMAP
    if connection.imap_use_ssl:
        imap = imaplib.IMAP4_SSL(connection.imap_server, connection.imap_port, timeout=10)
    else:
        imap = imaplib.IMAP4(connection.imap_server, connection.imap_port)

    try:
        imap.login(connection.username, pwd)
        imap.select(connection.imap_folder)
        status, data = imap.search(None, 'UNSEEN')
        if status != 'OK':
            raise RuntimeError(f"Erro no SEARCH IMAP: {status}")

        ids = data[0].split()
        count = 0
        for msg_id in ids:
            status, msg_data = imap.fetch(msg_id, '(RFC822)')
            if status != 'OK':
                continue
            raw = msg_data[0][1].decode('utf-8', errors='ignore')
            ingest_raw_email(db, raw)
            # marca como lido
            imap.store(msg_id, '+FLAGS', '\\Seen')
            count += 1

        return count

    finally:
        imap.logout()