import configparser
import importlib


def get_repositorio_cnpj(arquivo_configuracoes):
    cfg = configparser.ConfigParser()
    cfg.read_file(open(arquivo_configuracoes))
    RepositorioCNPJ = getattr(importlib.import_module(cfg['cnpj']['modulo']), cfg['cnpj']['classe'])
    return RepositorioCNPJ()


def get_dao_busca_textual(arquivo_configuracoes):
    cfg = configparser.ConfigParser()
    cfg.read_file(open(arquivo_configuracoes))
    DaoRFB = getattr(importlib.import_module(cfg['busca']['modulo_busca_textual']), cfg['busca']['dao_busca_textual'])
    return DaoRFB()
