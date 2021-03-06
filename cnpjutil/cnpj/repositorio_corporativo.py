import json
import re
from collections import defaultdict

import pyodbc
import requests
import unicodedata

from cnpjutil.cnpj import fabrica_provedor_cnpj
from cnpjutil.cnpj.api_lucene import buscar_em_api_lucene
from cnpjutil.cnpj.dao import DaoRFB
from cnpjutil.cnpj.repositorio import RepositorioCNPJ


def __remover_acentos(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def processar_descricao_contratado(descricao):
    descricao = descricao.strip()
    descricao = descricao.upper()

    # Remove espaços extras
    descricao = re.sub(' +', ' ', descricao)

    # Remove acentos
    # descricao = unidecode.unidecode(descricao)
    descricao = __remover_acentos(descricao)

    # Remova caracteres especiais
    descricao = descricao.replace('&', '').replace('/', '').replace('-', '').replace('"', '')

    return descricao


class RepositorioCNPJCorporativo(RepositorioCNPJ):
    def buscar_empresas_por_razao_social(self, razao_social):
        dao_sql = DaoRFB_SQLServer(self.arquivo_configuracoes)
        descricao = processar_descricao_contratado(razao_social)
        empresas, tipo_busca = dao_sql.buscar_empresa_por_razao_social(descricao)
        map_empresas_to_cnpjs = defaultdict(list)

        for cnpj, nome in empresas:
            map_empresas_to_cnpjs[nome].append(cnpj)

        # Caso não tenha encontrado nenhum resultado, utiliza como fallback o índice textual
        if len(empresas) == 0:
            dao_busca_textual = fabrica_provedor_cnpj.get_dao_busca_textual(self.arquivo_configuracoes)
            map_empresas_to_cnpjs, tipo_busca = dao_busca_textual.buscar_empresa_por_razao_social(descricao)

        return map_empresas_to_cnpjs, tipo_busca


class DaoRFB_SQLServer(DaoRFB):
    """
    Classe de acesso a uma base que contém os dados de pessoa jurídica disponibilizados pela Receita Federal do Brasil.
    """

    def __get_conexao(self):
        conn = pyodbc.connect('DRIVER={' + self.cfg.get("bd", "driver") + '};' +
                              f'SERVER={self.cfg.get("bd", "server")};Database={self.cfg.get("bd", "database")};'
                              f'UID={self.cfg.get("bd", "uid")};PWD={self.cfg.get("bd", "pwd")}')
        return conn

    def buscar_empresa_por_razao_social(self, nome):
        """
        Busca as empresas que possuam razão social idêntica ao nome passado como parâmetro.

        :param Nome procurado.
        :return As empresas que possuam razão social idêntica ao nome passado como parâmetro.
        """
        conexao = self.__get_conexao()

        with conexao:
            c = conexao.cursor()
            cursor = c.execute(
                "SELECT [num_cnpj], [nome] FROM [BD_RECEITA].[dbo].[CNPJ] WHERE [nome] = ? and [ind_matriz_filial] = ?",
                (nome, 1))
            resultado = cursor.fetchall()

        tipo_busca = ''

        if len(resultado) > 0:
            tipo_busca = "BUSCA EXATA RFB"

        return resultado, tipo_busca


class DaoRFB_BuscaTextualLucene(DaoRFB):
    def buscar_empresa_por_razao_social(self, nome):
        return buscar_em_api_lucene(nome, self.cfg['busca']['url_busca_lucene'])



