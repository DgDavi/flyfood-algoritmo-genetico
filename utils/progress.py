class Progress:
    @staticmethod
    def print_progress(fitness, best_cost, generation, population):
        if generation % 1 == 0:
            best = min(fitness)
            average = sum(fitness) / len(fitness)
            diversity = len({tuple(individual) for individual in population})

            print(
                f"Generation {generation:4d} | "
                f"best: {best} | "
                f"historical best: {best_cost} | "
                f"average: {average:.1f} | "
                f"distinct routes: {diversity}/{len(population)}"
            )
