from sys import exit


class MatrixParsing:
    @staticmethod
    def parse():
        file_object = open("edgesbrasil58.tsp")  # noqa

        distances = {}

        for i in range(1, 58):
            line = file_object.readline()
            
            values = line.split()

            for j in range(i+1, 59):
                if len(values) > 0:
                    weight = int(values.pop(0))
                else:
                    print(f"Error! Line {i} of the file does not have enough values.")
                    exit()

                distances[(i,j)] = weight
                distances[(j,i)] = weight

        file_object.close()

        return distances