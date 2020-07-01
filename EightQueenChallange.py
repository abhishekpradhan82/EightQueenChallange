import random 

# Number of individuals in each generation 
POPULATION_SIZE = 1000

# Valid genes 
GENES = '01234567'

# Target string to be generated 
TARGET_LENGTH = 8

MUTATE = 1

class Individual(object): 
    def __init__(self, chromosome): 
        self.chromosome = chromosome 
        self.fitness = self.calFitness() 

    @classmethod
    def mutatedGenes(self): 
        global GENES 
        gene = random.choice(GENES) 
        return gene 

    @classmethod
    def createGnome(self): 
        global TARGET_LENGTH 
        gnome_len = TARGET_LENGTH
        return [self.mutatedGenes() for _ in range(gnome_len)] 
    
    #This function identifies all the positions in a chess board wrt to a cell(irow,icol) which a Queen can HUNT
    def QueenAreas(self,irow,icol):
        posIndex = set()
        for i in range(-8,8):
            if (icol-i) >=0 and (icol-i) <=7 and (irow - i)<=7 and (irow - i)>=0:        
                pos = (irow - i)*10 + (icol-i)
                posIndex.add(pos)

        for i in range(-8,8):       
            if (icol+i)<=7 and (icol+i) >= 0 and (irow - i)<=7 and (irow - i)>=0:
                pos = (irow - i)*10 + (icol+i)
                posIndex.add(pos)

        for i in range(-8,8): 
            if (icol+i)<=7 and (icol+i) >= 0:
                pos = irow*10 + (icol+i)
                posIndex.add(pos)

        for i in range(-8,8): 
            if (irow+i)<=7 and (irow+i) >= 0:
                pos = (irow+i)*10 + icol
                posIndex.add(pos)

        return posIndex

    def mate(self, par2): 
        children = [] 
        threshold = len(self.chromosome)//2

        #Simple 50-50 Crossover
        child1 = self.chromosome[0:threshold] + par2.chromosome[threshold:]
        child2 = par2.chromosome[0:threshold] + self.chromosome[threshold:] 

        #randomely choose the gene to mutate
        mpos1 = random.choices(range(len(self.chromosome)-1), k=1)
        mpos2 = random.choices(range(len(self.chromosome)-1), k=1)

        #pick a random gene
        mchar1 = self.mutatedGenes()
        mchar2 = self.mutatedGenes()

        #murate
        child1[mpos1[0]] = mchar1
        child2[mpos2[0]] = mchar2

        ch1 = Individual(child1)
        ch2 = Individual(child2)
        
        children.append(ch1)
        children.append(ch2)         
        
        #return the two children
        return children 

    def calFitness(self):  
        fitness = 0
        fitness = self.checkQueenPosition(self.chromosome)
        return fitness 
    
    def checkQueenPosition(self,c1):
        fitness = 8
        cells = []
        for col in  range(len(c1)):
            cells.append((int(c1[col]), col))

        for i in range(len(cells)):
            currPosRange = self.QueenAreas(cells[i][0],cells[i][1])
            currPos = cells[i][0]*10 + cells[i][1]
            blnIsPerfect=True
            for j in range(len(cells)):
                checkPos = cells[j][0]*10 + cells[j][1]
                if currPos == checkPos:
                    continue

                if checkPos in currPosRange:
                    blnIsPerfect = False            
                    break;

            if blnIsPerfect:
                fitness = fitness - 1
                
        return fitness
    
    @classmethod
    def generateInitalPopulation(self):
        global POPULATION_SIZE
    
        population = [] 
        # create initial population 
        for _ in range(POPULATION_SIZE): 
            gnome = self.createGnome() 
            population.append(Individual(gnome)) 

        return population 
    
def main():     
    
    generation = 1

    found = False
    
    population = Individual.generateInitalPopulation()

    while not found:
        # sort the population in increasing order of fitness score 
        population = sorted(population, key = lambda x:x.fitness) 

        # if the individual having lowest fitness score ie. 
        # 0 then we know that we have reached to the target 
        # and break the loop 
        # 0 means we have found the sequence
        if population[0].fitness <= 0: 
            found = True
            break

        # Otherwise generate new offsprings for new generation 
        new_generation = [] 

        # Perform Elitism, that mean 10% of fittest population 
        # goes to the next generation 
        s = int((10*POPULATION_SIZE)/100) 
        new_generation.extend(population[:s]) 

        # From 50% of fittest population, Individuals 
        # will mate to produce 2 offsprings 
        s = int((90*POPULATION_SIZE)/100) 
        for _ in range(s): 
            parent1 = random.choice(population[:50]) 
            parent2 = random.choice(population[:50])            

            IndividualChildren = parent1.mate(parent2)
            new_generation.append(IndividualChildren[0]) 
            new_generation.append(IndividualChildren[1])
             

        population = new_generation 

        print("Generation: {}\tString: {}\tFitness: {}".format(generation,"".join(population[0].chromosome),population[0].fitness)) 

        generation += 1

    print("Generation: {}\tString: {}\tFitness: {}".format(generation,"".join(population[0].chromosome),population[0].fitness)) 

if __name__ == '__main__': 
    main()
