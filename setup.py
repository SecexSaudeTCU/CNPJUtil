from setuptools import setup

setup(
    name='cnpjutil',
    version='1.0',
    description='Módulo responsável por atuar como camada de acesso a dados de CNPJ, corporativos ou abertos',
    author='Monique Monteiro',
    author_email='moniquebm@tcu.gov.br',
    packages=['cnpjutil','cnpjutil.cnpj'],
    install_requires=['certifi', 'idna', 'pyodbc', 'requests', 'urllib3', 'wincertstore'],
)
