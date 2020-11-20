import configparser
from abc import ABC, abstractmethod

from cnpjutil.cnpj.api_lucene import buscar_em_api_lucene


class RepositorioCNPJ(ABC):
    def __init__(self, arquivo_configuracoes):
        self.arquivo_configuracoes = arquivo_configuracoes
        self.cfg = configparser.ConfigParser()
        self.cfg.read_file(open(arquivo_configuracoes))

    @abstractmethod
    def buscar_empresas_por_razao_social(self, razao_social):
        pass


class RepositorioCNPJAberto(RepositorioCNPJ):
    def __init__(self, arquivo_configuracoes):
        super().__init__(arquivo_configuracoes)

    def buscar_empresas_por_razao_social(self, razao_social):
        return buscar_em_api_lucene(razao_social, self.cfg['busca']['url_busca_lucene'])
