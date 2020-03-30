"""
Trata o contexto atual da busca
"""
from app.utils import get_str_data_formatada, is_feriado, is_atipico


class Contexto():
    def __init__(self, qtde_horarios=3):
        self.__orientacoes = set()

        self.qtde_horarios = qtde_horarios

        self.hora_atual = get_str_data_formatada('%H:%M')
        self.dia_semana = get_str_data_formatada('%a')
        self.feriado = is_feriado(get_str_data_formatada('%d/%m'))
        self.atipicos = is_atipico(get_str_data_formatada('%d/%m'))

    def get_proximos_horarios(self, lista_horarios):
        if not lista_horarios:
            return '\U0001F6AB Não opera'

        # Próximos horários
        prox_horarios = [partida
                         for partida in lista_horarios
                         if partida.hora > self.hora_atual][:self.qtde_horarios]
        # adicionando itens, caso já tenha chegado ao fim da lista
        if len(prox_horarios) < self.qtde_horarios:
            prox_horarios.extend(
                lista_horarios[:(self.qtde_horarios-len(prox_horarios))])

        str_prox_horarios = ''
        for partida in prox_horarios:
            str_prox_horarios += partida.hora.strip()
            if partida.orientacao:
                self.__orientacoes.add(partida.orientacao)
                str_prox_horarios += partida.orientacao.strip()
            str_prox_horarios += ' '

        return str_prox_horarios

    def is_dia_util(self):
        return (not self.feriado and
                not self.atipicos and
                self.dia_semana != 'Sat' and
                self.dia_semana != 'Sun')

    def is_sabado(self):
        return (not self.feriado and
                not self.atipicos and
                self.dia_semana == 'Sat')

    def is_domingo(self):
        return (self.feriado or
                self.dia_semana == 'Sun')

    def is_atipico(self):
        return self.atipicos

    def is_valido(self):
        return (self.hora_atual and
                self.dia_semana and
                self.feriado is not None and
                self.atipicos is not None)

    def __str__(self):
        return '''
        qtde_horarios: {}
        hora_atual: {}
        dia_semana: {}
        feriado: {}
        atípicos: {}
        '''.format(self.qtde_horarios,
                   self.hora_atual,
                   self.dia_semana,
                   self.feriado,
                   self.atipicos)
