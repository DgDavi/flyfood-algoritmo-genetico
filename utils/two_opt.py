
class LocalSearch:
    @staticmethod
    def two_opt(route, distances, max_passes=100):
        best_route = route[:]
        n = len(best_route)

        if n < 4:
            return best_route

        for _ in range(max_passes):
            improved = False

            # Keep the first city fixed.
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    a = best_route[i - 1]
                    b = best_route[i]
                    c = best_route[j]
                    d = best_route[(j + 1) % n]

                    old_cost = (
                        distances[(a, b)] +
                        distances[(c, d)]
                    )

                    new_cost = (
                        distances[(a, c)] +
                        distances[(b, d)]
                    )

                    if new_cost < old_cost:
                        best_route[i:j + 1] = reversed(
                            best_route[i:j + 1]
                        )
                        improved = True
                        break

                if improved:
                    break

            if not improved:
                break

        return best_route
