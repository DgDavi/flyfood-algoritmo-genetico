from sys import exit


class CostPath:
    @staticmethod
    def calculate(permutation, distances):
        total = 0
        for i in range(len(permutation)-1):
            a = permutation[i]
            b = permutation[i+1]
            if (a,b) in distances:
                total += distances[(a,b)]
            else:
                print(f"Error! ({a},{b}) does not exist in the dictionary!")
                exit()

        total += distances[(permutation[-1],permutation[0])]
        return total