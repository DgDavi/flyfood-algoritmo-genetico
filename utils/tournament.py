import random

from core.parameters import TORNEIO


class Tournament:

    @staticmethod
    def play(populacao, aptidoes, k=TORNEIO) :

        if len(populacao) != len(aptidoes):
            raise ValueError("População e aptidões devem ter o mesmo tamanho.")

        if not 1 <= k <= len(populacao):
            raise ValueError("TORNEIO deve estar entre 1 e o tamanho da população.")
        
        candidatos = random.sample(range(len(populacao)), k)

        melhor = min(candidatos, key=lambda idx: aptidoes[idx])
        
        return populacao[melhor]