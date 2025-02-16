import random
from .ga_bird import GABird

def crossover(parent1, parent2):
    """
    Perform crossover between two parent networks.
    For each gene in the flattened weight vector, choose the gene from parent1
    with a 50% chance; otherwise, choose it from parent2.
    
    Returns:
        A new NeuralNetwork instance constructed from the resulting weight vector.
    """
    vec1 = parent1.network.to_vector()
    vec2 = parent2.network.to_vector()
    child_vec = [vec1[i] if random.random() < 0.5 else vec2[i] for i in range(len(vec1))]
    from .neural_network import NeuralNetwork  # Local import to avoid circular dependencies
    return NeuralNetwork(child_vec)

def mutate(network, mutation_rate=0.1, mutation_strength=0.5):
    """
    Mutate the network's weights by adding Gaussian noise to each gene with
    a given probability (mutation_rate). The noise is sampled from a normal distribution
    with standard deviation mutation_strength.
    
    Returns:
        A new NeuralNetwork instance with the mutated weight vector.
    """
    vec = network.to_vector()
    mutated_vec = [gene + random.gauss(0, mutation_strength) if random.random() < mutation_rate else gene for gene in vec]
    from .neural_network import NeuralNetwork
    return NeuralNetwork(mutated_vec)

def evolve(population):
    """
    Evolve the given population of GABird instances using elitism and genetic operators.
    
    Steps:
        1. Sort birds by fitness (highest first).
        2. Keep the top 10% (at least 5 birds) as elites.
        3. Clone the elite birds.
        4. Generate offspring via crossover and mutation until the population size is restored.
    
    Returns:
        A new population of GABird instances.
    """
    population.sort(key=lambda bird: bird.fitness, reverse=True)
    new_population = []
    elite_count = max(5, int(0.1 * len(population)))
    elites = population[:elite_count]
    
    # Clone elite birds
    for bird in elites:
        new_population.append(GABird(bird.network))
    
    # Generate offspring until population is restored
    while len(new_population) < len(population):
        parent1 = random.choice(elites)
        parent2 = random.choice(elites)
        child_network = crossover(parent1, parent2)
        child_network = mutate(child_network)
        new_population.append(GABird(child_network))
    
    return new_population
