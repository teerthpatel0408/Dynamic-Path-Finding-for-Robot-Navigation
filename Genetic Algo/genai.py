import numpy as np
import pygame
import time
import operator

class MazeNavigator:
    def __init__(self, dna_size):
        # Initialize the navigator with a DNA size
        self.dna_size = dna_size
        self.dna = []
        self.distance = 0.0
        self.pos_x = 0
        self.pos_y = 0
        self.color = (0, 255, 128)  # Color representation # this is mutation + first generation
        
        # Generate random DNA sequence for the navigator
        for _ in range(self.dna_size):
            self.dna.append(np.random.randint(0, 4))

    def move(self, speed_x, speed_y):
        # Move the navigator based on speed
        self.pos_x += speed_x
        self.pos_y += speed_y

class MazeEnvironment:
    def __init__(self):
        # Initialize the maze environment parameters
        self.width = 400
        self.height = 400
        self.n_rows = 20
        self.n_columns = 20
        self.population_size = 100
        self.dna_size = 400
        self.best_copied = 20
        self.mutation_rate = 0.1
        self.offspring_mutation_rate = 0.10
        self.wait_time = 0.05
        self.slowdown_rate_of_change = 0.005
        self.wall_ratio = 0.2

        # Define start and goal positions
        self.start_x = 0 # Start position x-coordinate
        self.start_y = 0 # Start position y-coordinate
        self.goal_x = self.n_columns - 1 # Goal position x-coordinate
        self.goal_y = self.n_rows - 1 # Goal position y-coordinate

        self.population = []
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.maze = np.zeros((self.n_rows, self.n_columns))

        # if self.bestCopied > self.populationSize:
        #     self.bestCopied = self.populationSize
        
        # Initialize maze with walls
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if np.random.rand() < self.wall_ratio:
                    self.maze[i][j] = 1
                else:
                    self.maze[i][j] = 0

        # Set a clear path from start to goal
        for i in range(min(3, self.n_rows)):
            for j in range(min(3, self.n_columns)):
                self.maze[i][j] = 0

        # Create a population of navigators
        for i in range(self.population_size):
            navigator = MazeNavigator(self.dna_size)
            navigator.pos_x = self.start_x
            navigator.pos_y = self.start_y
            self.population.append(navigator)

        self.start_color = (255, 150, 50)  # Orange color for start state
        self.goal_color = (255, 150, 50)  # Orange color for goal state
        self.goal_reached = False

    def draw_maze(self):
        # Draw the maze and navigators on the screen
        cell_width = self.width / self.n_columns
        cell_height = self.height / self.n_rows

        self.screen.fill((0, 0, 0))

        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(self.screen, (186, 180, 182), (j * cell_width, i * cell_height, cell_width, cell_height))
                if i == self.start_y and j == self.start_x:
                    pygame.draw.rect(self.screen, self.start_color, (j * cell_width, i * cell_height, cell_width, cell_height))
                if i == self.goal_y and j == self.goal_x:
                    pygame.draw.rect(self.screen, self.goal_color, (j * cell_width, i * cell_height, cell_width, cell_height))

        for bot in self.population:
            pygame.draw.rect(self.screen, bot.color, (bot.pos_x * cell_width, bot.pos_y * cell_height, cell_width, cell_height))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.wait_time -= self.slowdown_rate_of_change
                    if self.wait_time < 0:
                        self.wait_time = 0
                    print('Wait time lowered to {:.3f}'.format(self.wait_time))
                elif event.key == pygame.K_s:
                    self.wait_time += self.slowdown_rate_of_change
                    print('Wait time increased to {:.3f}'.format(self.wait_time))

    def step(self, n_action):
        # Move navigators based on their DNA sequence
        if not self.goal_reached:
            for bot in self.population:
                if bot.dna[n_action] == 0:
                    if bot.pos_y > 0:
                        if self.maze[bot.pos_y - 1][bot.pos_x] == 0:
                            bot.move(0, -1)
                elif bot.dna[n_action] == 1:
                    if bot.pos_y < self.n_rows - 1:
                        if self.maze[bot.pos_y + 1][bot.pos_x] == 0:
                            bot.move(0, 1)
                elif bot.dna[n_action] == 2:
                    if bot.pos_x < self.n_columns - 1:
                        if self.maze[bot.pos_y][bot.pos_x + 1] == 0:
                            bot.move(1, 0)
                elif bot.dna[n_action] == 3:
                    if bot.pos_x > 0:
                        if self.maze[bot.pos_y][bot.pos_x - 1] == 0:
                            bot.move(-1, 0)

                if bot.pos_x == self.goal_x and bot.pos_y == self.goal_y:
                    self.goal_reached = True

            self.draw_maze()
            time.sleep(self.wait_time)

    def mix(self, dna1, dna2):
        # Mix DNA from two parents to create offspring
        offspring = MazeNavigator(self.dna_size)
        for i in range(self.dna_size):
            if np.random.rand() > self.offspring_mutation_rate:
                if np.random.randint(0, 2) == 0:
                    offspring.dna[i] = dna1[i]
                else:
                    offspring.dna[i] = dna2[i]
            else:
                offspring.dna[i] = np.random.randint(0, 4)

        return offspring

    def create_new_population(self, gen, iter1):
        # Create a new population of navigators based on the performance of the previous generation
        if not self.goal_reached:
            sorted_population = sorted(self.population, key=operator.attrgetter('distance'), reverse=True)
            self.population.clear()

            best_result = sorted_population[0].distance
            available = self.population_size - self.best_copied + 5 * iter1 #increasing the size of the population with end of each generation by 5 to increase the chances of the population to survive and reach the goal state successfully.

            for i in range(self.best_copied):
                best = sorted_population[i]
                best.pos_x = self.start_x
                best.pos_y = self.start_y
                best.distance = 0.0
                best.color = (0, 102, 230)  # Top 10% from the previous generation #BLUE
                self.population.append(best)

            for i in range(available):
                new = MazeNavigator(self.dna_size)
                if np.random.rand() > self.mutation_rate:
                    p1rnd = np.random.randint(0, self.best_copied)
                    parent1 = sorted_population[p1rnd]

                    p2rnd = np.random.randint(0, self.best_copied)
                    while p2rnd == p1rnd:
                        p2rnd = np.random.randint(0, self.best_copied)
                    parent2 = sorted_population[p2rnd]

                    dna1 = parent1.dna
                    dna2 = parent2.dna

                    new = self.mix(dna1, dna2)
                    new.color = (153, 204, 255)  # This is the new generation #light blue

                self.population.append(new)

            print('Generation: ' + str(gen) + ' Population Size: ' + str(len(self.population)))

# Initialize the environment
env = MazeEnvironment()
n_action = 0
gen = 0
iter1 = 0
pygame.init()

# Run the simulation until the goal is reached
while not env.goal_reached:
    if n_action < env.dna_size:
        env.step(n_action)
        n_action += 1
    else:
        gen += 1
        n_action = 0
        env.create_new_population(gen, iter1)
        iter1 += 1

# Display the final best path
while True:
    env.draw_maze()