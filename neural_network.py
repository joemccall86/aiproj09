from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
import math


class NeuralNetwork():
    
    def __init__(self):
        # We will be using this later, I'm just anal about it right now.
        self.pop = None

        # needed for pyneat
        config.load('ai_config')
        
        # Temporary workaround
        chromosome.node_gene_type = genome.NodeGene
        
    def nextGeneration(self, brains, listOfTargets, listOfPositions):
        """
        Brains is a list of chromosomes that we need to copy into a population.
        This function returns a new list of chromosomes (the next generation)
        """
        numBrains = len(brains)
        assert(numBrains == len(listOfTargets))
        assert(numBrains == len(listOfPositions))
        
        # TODO find a faster way to do this
        if None == self.pop:
            self.pop = population.Population()
        self.pop.setPop(brains)
        
        # Note that this function should be as streamlined as possible
        def fitness(population):
            # We don't need to check the network itself. We just need to check
            # the distance between the current brain and the current target
            assert(numBrains == len(population))
            for i,chromo in enumerate(population):
                x1, y1 = listOfPositions[i]
                x2, y2 = listOfTargets[i]
                
                distance = math.hypot(x2-x1, y2-y1)
                # Since we want to minimize distance, just make the fitness the negative of the distance
                chromo.fitness = 500 - distance
        
        # Point the fitness function to the one we just defined
        population.Population.evaluate = fitness
        
        # One epoch
        self.pop.rt_epoch()
        
        return self.pop.getPop()
        
if __name__ == "__main__":
    nn = NeuralNetwork()
    print("compiled good")