import configparser
from abc import ABC, abstractmethod


class DaoBase(ABC):
    def __init__(self, arquivo_configuracoes):
        """
        Construtor da classe.
        """
        self.cfg = configparser.ConfigParser(interpolation=None)
        self.cfg.read_file(open(arquivo_configuracoes))


class DaoRFB(DaoBase):

    @abstractmethod
    def buscar_empresa_por_razao_social(self, nome):
        pass
