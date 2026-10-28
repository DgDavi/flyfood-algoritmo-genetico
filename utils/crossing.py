from deap import tools


class Crossing:
    @staticmethod
    def play(pai1, pai2):
        filho1 = [cidade - 1 for cidade in pai1]
        filho2 = [cidade - 1 for cidade in pai2]

        tools.cxOrdered(filho1, filho2)
        
        filho1 = [cidade + 1 for cidade in filho1]
        filho2 = [cidade + 1 for cidade in filho2]

        return filho1, filho2