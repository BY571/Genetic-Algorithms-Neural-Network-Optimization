import numpy as np
import random
import matplotlib.pyplot as plt
import argparse

# class to creat a population of random members
class Member():
  def __init__(self,length,DNA_pool, DNA = None):
    
    self.DNA_pool = DNA_pool # traits or "DNA-Pool"
    # final DNA length
    self.length = length
    
    # actual/ final DNA 
    if DNA and len(DNA) == self.length:
      self.DNA = DNA
    else:
      self.DNA = ""
      
    self.fitness = 0.
    
  def create(self):
    for i in range(self.length):
      self.DNA += random.choice(self.DNA_pool)
      
  def print_DNA(self):
    print(self.DNA)
    
  def calc_fitness(self, goal):
    # Calculating the fitness by checking how many characters/DNA/traits already match
    for i, elem in enumerate(self.DNA):  
      if str(elem) == goal[i]:
        self.fitness += 1
  
  def mutate(self,mutation_rate):
    for i in range(len(self.DNA)):
      if np.random.random() < mutation_rate:

        DNA_list = list(self.DNA)
        DNA_list[i] = random.choice(self.DNA_pool)
        self.DNA = "".join(DNA_list) 


def show_best_member(population,norm_pop):
  idx = np.argmax(norm_pop)
  member = population[idx]
  member.print_DNA()
  
def normalize_fitness(population):
  # Normalizing the fitness of the population for a Probalistic Selection
  population_fitness= [i.fitness for i in population]
  norm_fit = []
  for mem in population:
    if sum(population_fitness) != 0:
      norm = mem.fitness/sum(population_fitness)
    else:
      norm = 0
    norm_fit.append(norm)
  return norm_fit

def crossover(population, norm_pop):
    """ 
    Midpoint_Corssover method
    returns the DNA or new name of the child after crossover
    """
    #selects two parents probabilistic accroding to the fitness
    if sum(norm_pop) != 0:
      parent1 = np.random.choice(population, p = norm_pop)
      parent2 = np.random.choice(population, p = norm_pop)
    else:
      # if there are no "best" parents choose randomly 
      parent1 = np.random.choice(population)
      parent2 = np.random.choice(population)
    
    # picking random midpoint for crossing over name/DNA
    #print(parent1)
    mid_point = np.random.choice([i for i in range(len(parent1.DNA))])
    # adding DNA-Sequences of the parents to final DNA
    child_DNA = parent1.DNA[:mid_point] + parent2.DNA[mid_point:]
    return child_DNA

def reproduction(population, norm_pop,DNA_pool,DNA_length, mutation_rate):
  """
  Reproduces the Population with Crossover and Mutation
  
  Returns the new Population
  """
  new_population = []
  for n in range(len(population)):
    # CROSSOVER
    child_DNA = crossover(population, norm_pop)
    child = Member(DNA_length, DNA_pool, DNA = child_DNA)
    # Mutation
    child.mutate(mutation_rate)
    new_population.append(child)
  return new_population


def init_population(population_size,DNA_pool,DNA_length):
  """
  Creates the initial Population:
  """
  population = []
  for mem in range(population_size):
    mem = Member(DNA_length, DNA_pool)
    mem.create()
    population.append(mem)
  return population

def plotting(histogram_plot, mean_plot,max_plot,min_plot,goal_value):
  
  plt.subplot(122)
  plt.title("Single member fitness")
  bar_ = plt.bar(np.linspace(1,len(histogram_plot),num=len(histogram_plot)),histogram_plot)
  mean1 = np.mean(histogram_plot)
  goal_, = plt.plot(np.resize(mean1,len(histogram_plot)),"r")
  plt.legend([bar_,goal_],["fitness","mean"])
  plt.subplot(121)
  plt.title("Overall statistics")
  plt.ylabel("Fitness")
  plt.xlabel("Generation")
  max_, = plt.plot(max_plot)
  min_, = plt.plot(min_plot)
  mean_, = plt.plot(mean_plot)
  goal_, = plt.plot(np.resize(goal_value,len(mean_plot)))
  plt.legend([max_,min_,mean_,goal_],["Max","Min","Mean","Optimum"])
  plt.show()
  plt.pause(0.001)
  plt.clf()

def genetic_algorithm( population_size,DNA_pool,goal, mutation_rate):
  DNA_length = len(goal)
  # initialize first population
  population = init_population(population_size, DNA_pool, DNA_length)
  done = False
  episode    = 0
  mean_plot = []
  max_plot = []
  min_plot = []
  goal_value = len(list(goal))
  while not done:
    
    # Checking if goal reached:
    for member in population:
      if member.DNA == goal:
        print("Evolution goal reached!!!")
        print("Final answer: ")
        member.print_DNA()
        print("-------------------------")
        print("Do you want to end evolution?")
        input_ = input("[y/n]")
        if input_ == "y":
          exit()
        else:
          pass
    # calc_fitness:
    histogram_plot = []
    for member in population:
      member.calc_fitness(goal)
      histogram_plot.append(member.fitness)
    normalized_fitness = normalize_fitness(population)
    ### PRINT BEST MEMBER of current Population
    print("Population: {}, best member: ".format(episode))
    show_best_member(population, normalize_fitness)
    print("\nReproduction!")
    
    new_population = reproduction(population,normalized_fitness,DNA_pool,DNA_length, mutation_rate)
    population = new_population
    print("Death of the parents!")
    print("-------------------\n")
    episode += 1
    mean_plot.append(np.mean(histogram_plot))
    max_plot.append(max(histogram_plot))
    min_plot.append(min(histogram_plot))
    #Plotting
    #print(histogram_plot)
    plotting(histogram_plot,mean_plot,max_plot,min_plot,goal_value)

def main(population_size,goal,mutation_rate):
  #goal = "this is sparta!"
  # define the traits you want to vary on // DNA!
  traits = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","?","!"," "]
  plt.ion()
  fig = plt.figure()
  genetic_algorithm(population_size = population_size,DNA_pool = traits, goal = goal, mutation_rate = mutation_rate)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--Population_size",type = int,default = 50, help="Size of the Population- how many members per Population")
  parser.add_argument("-g", "--Goal",type = str,default = "genetic algorithm", help = "Sequenz of characters as the goal DNA to reach -- has to be lower case!")
  parser.add_argument("-m", "--Mutation_rate", type  = float, default = 0.015, help = "Percentage of how probably it is that mutation occures")
  args = parser.parse_args()
  main(args.Population_size,args.Goal,args.Mutation_rate)