from random import choice, randint
from TA.subset.ISubset import ISubsetSelector
from utils.global_props import SAMPLE_SIZE, get_sample_attempts


class GenecticEvolution(ISubsetSelector):
    def __repr__(self):
        return "GenecticEvolution"

    def load(self, all_data_zip, true_data_zip, false_data_zip) -> ISubsetSelector:
        self.all_data_zip = all_data_zip
        self.true_data_zip = true_data_zip
        self.false_data_zip = false_data_zip
        self.sample_size = SAMPLE_SIZE
        self.EVOLUTION_EPOCHS = 50

        self.population = self.init_population()
        self.evaluation_queue = self.population

        self.prev_candidate = None
        self.canidate_evaluation_map = {}

    def init_population(self):
        """Generate the initial population"""
        total_iterations = get_sample_attempts()
        population_size = total_iterations // self.EVOLUTION_EPOCHS  # evolution itterations

        population = []
        for i in range(0, population_size):
            population.append(self.random_canidate())

        return population

    def random_canidate(self):
        """Get a random canidate"""
        picks = []
        while(len(picks) < self.sample_size):
            to_add = choice(self.all_data_zip)
            aX, aY, aL = to_add
            found_match = False
            for pX, pY, pL in picks:
                if (pX == aX).all() and (pY == aY).all() and pL == aL:
                    found_match = True
                    break
            if found_match:
                continue

            picks.append(to_add)
        return picks

    def evaluate_and_create_new_population(self):
        """We sample from the population based on fitness. To do this we will use q-tournament, in 2-tournament style"""
        # create a pool to find which elements gets removed
        sampled_population = []
        Q = 2  # tournament size
        # sample the population to survive
        for i in range(sampled_population.size()):
            in_tournament = []
            for j in range(Q):
                in_tournament.append(choice(self.population))

            winner = max(
                in_tournament, key=lambda x: self.canidate_evaluation_map[x])
            sampled_population.append(winner)

        all_data_points_in_population = []
        for canidate in sampled_population:
            for elem in canidate:
                all_data_points_in_population.append(elem)

        mutadated_population = []
        # Next we mutate the population to get some variation
        for candidate in sampled_population:
            mutated_canidate = None
            while True:
                outcome = randint(0, 100)
                mutation_chance = 15
                if outcome <= 100-mutation_chance:  # Do nothing
                    mutated_canidate = candidate
                    break
                else:
                    cross_breed = 66
                    complete_new = 100-cross_breed
                    outcome = randint(0, 100)
                    if outcome <= cross_breed:  # Crossbreed with population
                        index_to_swap = randint(0, len(candidate)-1)
                        canidate[index_to_swap] = choice(
                            all_data_points_in_population)
                    else:
                        index_to_swap = randint(0, len(candidate)-1)
                        canidate[index_to_swap] = choice(self.all_data_zip)
            mutadated_population.append(mutated_canidate)

        # set new population
        self.population = self.mutadated_population
        self.evaluation_queue = self.population
        self.prev_candidate = None
        self.canidate_evaluation_map = {}

    def get_next_subset(self, previus_score, previus_subset):
        if self.prev_candidate is not None:
            self.canidate_evaluation_map[self.prev_candidate] = previus_score
        if len(self.evaluation_queue) == 0:
            self.evaluate_and_create_new_population()
        current_canidate = self.evaluation_queue.pop()
        return current_canidate
