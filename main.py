from MetaheuristicAlgorithm import MetaheuristicAlgorithm

if __name__ == '__main__':
    algorithm = MetaheuristicAlgorithm("data/gifts.csv", "data/submission.csv")
    algorithm.create_initial_tsp()
