from setuptools import setup, find_packages

setup(
    name="leafcheck",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
        "SQLAlchemy",
        "alembic",
        "python-dotenv",
    ],
) 