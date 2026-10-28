
class LocalSearch:
    @staticmethod
    def two_opt(rota, distancias, max_passagens=100):
        melhor_rota = rota[:]
        n = len(melhor_rota)

        if n < 4:
            return melhor_rota

        for _ in range(max_passagens):
            melhorou = False

            # Mantém a primeira cidade fixa.
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    a = melhor_rota[i - 1]
                    b = melhor_rota[i]
                    c = melhor_rota[j]
                    d = melhor_rota[(j + 1) % n]

                    custo_antigo = (
                        distancias[(a, b)] +
                        distancias[(c, d)]
                    )

                    custo_novo = (
                        distancias[(a, c)] +
                        distancias[(b, d)]
                    )

                    if custo_novo < custo_antigo:
                        melhor_rota[i:j + 1] = reversed(
                            melhor_rota[i:j + 1]
                        )
                        melhorou = True
                        break

                if melhorou:
                    break

            if not melhorou:
                break

        return melhor_rota
