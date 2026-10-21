from utils import CostPath


class Fitness:
    @staticmethod
    def calculate(populacao, dicDistancias):
        listaAptidao = []
       
        for elem in populacao:
            listaAptidao.append(CostPath.calculate(elem, dicDistancias))
       
        return listaAptidao