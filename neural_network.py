from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
import math


class NeuralNetwork():
    
    def __init__(self):
        # We will be using this later, I'm just anal about it right now.
        pop = None

        # needed for pyneat
        config.load('ai_config')
        
        # Temporary workaround
        chromosome.node_gene_type = genome.NodeGene
        
    def nextGeneration(self, brains, listOfTargets, listOfPositions):
        """
        Creates the next generation of brains and returns them as a list.
        Takes in a list of brains, and a list of inputs for the neural network
        """
        numBrains = len(brains)
        assert(numBrains == len(listOfTargets))
        assert(numBrains == len(listOfPositions))
        
        # Note that this function should be as streamlined as possible
        def fitness(population):
            # We don't need to check the network itself. We just need to check
            # the distance between the current brain and the current target
            assert(numBrains == len(population))
            for i,chromo in enumerate(population):
                x1, y1 = listOfPositions[i]
                x2, y2 = listOfTargets[i]
                
                distance = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
                # Since we want to minimize distance, just make the fitness the negative of the distance
                chromo.fitness = -distance
        
        population.Population.evaluate = fitness
        if None == self.pop:
            self.pop = population.Population()
        
        # One epoch
        pop.rt_epoch()
        
if __name__ == "__main__":
    nn = NeuralNetwork()
    print("compiled good")