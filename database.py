from pony.orm import Database, Required, Optional
from datetime import datetime

db = Database()

class ResultadoSimulacao(db.Entity):
    tipo_mapa = Required(str)
    linhas = Required(int)
    colunas = Required(int)
    num_bombas = Required(int)
    vitorias_logico = Required(int)
    vitorias_random = Required(int)
    empates = Required(int)
    pontos_logico = Required(int)
    pontos_random = Required(int)
    quantidade_partidas = Required(int)
    data_hora = Required(datetime, default=datetime.now)

db.bind(provider='sqlite', filename='resultados.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
