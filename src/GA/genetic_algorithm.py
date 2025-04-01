# import random
# from .ga_bird import GABird
# from .neural_network import NeuralNetwork

# def tournament_selection(population, tournament_size=3):
#     """
#     Select one individual from the population using tournament selection.
#     Randomly chooses 'tournament_size' individuals and returns the one with the highest fitness.
#     """
#     tournament = random.sample(population, tournament_size)
#     tournament.sort(key=lambda bird: bird.fitness, reverse=True)
#     return tournament[0]

# def arithmetic_crossover(parent1, parent2):
#     """
#     Perform arithmetic crossover between two parent networks.
#     Rather than a simple gene-by-gene selection, we blend the parents' genes using a random weight alpha.
    
#     Returns:
#         A new NeuralNetwork instance constructed from the blended weight vector.
#     """
#     vec1 = parent1.network.to_vector()
#     vec2 = parent2.network.to_vector()
#     alpha = random.random()  # random coefficient between 0 and 1
#     child_vec = [alpha * vec1[i] + (1 - alpha) * vec2[i] for i in range(len(vec1))]
#     return NeuralNetwork(child_vec)

# def adaptive_mutation(network, mutation_rate=0.1, mutation_strength=0.5):
#     """
#     Mutate the network's weights by adding Gaussian noise to each gene with a given probability.
#     You could later adapt mutation_strength based on generation or fitness if desired.
    
#     Returns:
#         A new NeuralNetwork instance with the mutated weight vector.
#     """
#     vec = network.to_vector()
#     mutated_vec = [
#         gene + random.gauss(0, mutation_strength) if random.random() < mutation_rate else gene 
#         for gene in vec
#     ]
#     return NeuralNetwork(mutated_vec)

# def evolve(population, tournament_size=3, elite_fraction=0.1):
#     """
#     Evolve the given population of GABird instances using advanced genetic operators.
    
#     Steps:
#       1. Sort birds by fitness (highest first).
#       2. Preserve the top elite_fraction (at least 5 individuals) as elites.
#       3. Use tournament selection for parent selection.
#       4. Use arithmetic crossover and adaptive mutation to generate offspring until population size is restored.
    
#     Returns:
#       A new population of GABird instances.
#     """
#     population.sort(key=lambda bird: bird.fitness, reverse=True)
#     new_population = []
#     elite_count = max(5, int(elite_fraction * len(population)))
#     elites = population[:elite_count]
    
#     # Preserve elites directly (cloning them)
#     for bird in elites:
#         new_population.append(GABird(bird.network))
    
#     # Generate offspring using tournament selection, arithmetic crossover, and adaptive mutation.
#     while len(new_population) < len(population):
#         parent1 = tournament_selection(population, tournament_size)
#         parent2 = tournament_selection(population, tournament_size)
#         child_network = arithmetic_crossover(parent1, parent2)
#         child_network = adaptive_mutation(child_network, mutation_rate=0.1, mutation_strength=0.5)
#         new_population.append(GABird(child_network))
    
#     return new_population


import random
from .ga_bird import GABird
from .neural_network import NeuralNetwork

def tournament_selection(population, tournament_size=3):
    """
    Select one individual from the population using tournament selection.
    Randomly chooses 'tournament_size' individuals and returns the one with the highest fitness.
    """
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda bird: bird.fitness, reverse=True)
    return tournament[0]

def arithmetic_crossover(parent1, parent2):
    """
    Perform arithmetic crossover between two parent networks.
    Instead of choosing gene-by-gene, we blend the genes using a random coefficient.
    
    Returns:
        A new NeuralNetwork instance constructed from the blended weight vector.
    """
    vec1 = parent1.network.to_vector()
    vec2 = parent2.network.to_vector()
    alpha = random.random()  # random coefficient between 0 and 1
    child_vec = [alpha * vec1[i] + (1 - alpha) * vec2[i] for i in range(len(vec1))]
    return NeuralNetwork(child_vec)

def adaptive_mutation(network, mutation_rate=0.1, mutation_strength=0.5):
    """
    Mutate the network's weights by adding Gaussian noise to each gene with a given probability.
    (Adaptive mutation strategies can later modify the mutation_strength based on generation/fiteness.)
    
    Returns:
        A new NeuralNetwork instance with the mutated weight vector.
    """
    vec = network.to_vector()
    mutated_vec = [
        gene + random.gauss(0, mutation_strength) if random.random() < mutation_rate else gene
        for gene in vec
    ]
    return NeuralNetwork(mutated_vec)

def evolve(population, tournament_size=3, elite_fraction=0.1):
    """
    Evolve the given population of GABird instances using advanced genetic operators.
    
    Steps:
      1. Sort birds by fitness (highest first).
      2. Preserve the best individual (with highest fitness) unchanged.
      3. Preserve a fraction of elites (at least 5 individuals) as a secondary elite pool.
      4. Use tournament selection on the whole population for parent selection.
      5. Generate offspring via arithmetic crossover and adaptive mutation until the population size is restored.
    
    The best individual is always forwarded unchanged to maintain the highest fitness gene.
    
    Returns:
      A new population of GABird instances.
    """
    # Sort population so that best is first.
    population.sort(key=lambda bird: bird.fitness, reverse=True)
    new_population = []

    # Always preserve the very best individual (strict elitism)
    best_bird = population[0]
    new_population.append(GABird(best_bird.network))
    
    # Determine elite pool count (ensure at least 5)
    elite_count = max(5, int(elite_fraction * len(population)))
    elites = population[:elite_count]
    
    # Preserve additional elites (beyond the best already added)
    for bird in elites[1:]:
        new_population.append(GABird(bird.network))
    
    # Generate the remaining offspring until population size is restored.
    while len(new_population) < len(population):
        parent1 = tournament_selection(population, tournament_size)
        parent2 = tournament_selection(population, tournament_size)
        child_network = arithmetic_crossover(parent1, parent2)
        child_network = adaptive_mutation(child_network, mutation_rate=0.1, mutation_strength=0.5)
        new_population.append(GABird(child_network))
    
    return new_population
