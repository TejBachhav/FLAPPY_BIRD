import random
from .ga_bird import GABird

def crossover(parent1, parent2):
    vec1 = parent1.network.to_vector()
    vec2 = parent2.network.to_vector()
    child_vec = []
    for i in range(len(vec1)):
        # With 50% chance pick gene from parent1 or parent2
        child_vec.append(vec1[i] if random.random() < 0.5 else vec2[i])
    from .neural_network import NeuralNetwork
    return NeuralNetwork(child_vec)

def mutate(network, mutation_rate=0.1, mutation_strength=0.5):
    vec = network.to_vector()
    for i in range(len(vec)):
        if random.random() < mutation_rate:
            vec[i] += random.gauss(0, mutation_strength)
    from .neural_network import NeuralNetwork
    return NeuralNetwork(vec)

def evolve(population):
    # Sort birds by fitness (highest first)
    population.sort(key=lambda bird: bird.fitness, reverse=True)
    new_population = []
    # Elitism: keep top 10% (at least 5)
    elite_count = max(5, int(0.1 * len(population)))
    elites = population[:elite_count]
    for bird in elites:
        # Clone elite birds
        new_population.append(GABird(bird.network))
    # Generate offspring until population is full
    while len(new_population) < len(population):
        parent1 = random.choice(elites)
        parent2 = random.choice(elites)
        child_network = crossover(parent1, parent2)
        child_network = mutate(child_network)
        new_population.append(GABird(child_network))
    return new_population
