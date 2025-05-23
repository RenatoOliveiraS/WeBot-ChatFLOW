from setuptools import find_packages, setup

setup(
    name="webot-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=1.0.0",
        "redis>=5.0.0",
    ],
    python_requires=">=3.10",
)
