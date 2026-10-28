from sys import exit


class MatrixParsing:
    @staticmethod
    def parse():
        objArq = open("edgesbrasil58.tsp")  # noqa

        distancias = {}

        for i in range(1, 58):
            linha = objArq.readline() 
            
            lista = linha.split() 

            for j in range(i+1, 59):
                if len(lista) > 0:
                    peso = int(lista.pop(0)) 
                else:
                    print(f"Erro! linha {i} do arquivo não possui elementos suficientes")
                    exit()

                distancias[(i,j)] = peso
                distancias[(j,i)] = peso

        objArq.close()

        return distancias