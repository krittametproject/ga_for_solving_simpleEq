from random import randint as rnd
import random
import copy 
import math

""" SOLVING a, b, c, d in equation 2a+4b+3c-2d=41 """

def genR(len_chromosome):
    return [round(random.random(), 4) for _ in  range(len_chromosome)]

def gen_Algorithm(crsOver_rate, perMut_rate):
    temp_Round = []
    # gen Chromosome
    Round_number = 0  # temp round
    Chromosome = [[rnd(1, 41), rnd(1, 41), rnd(1, 41), rnd(1, 41)] for _ in range(6)]  # init Chromosome

    while True:
        Round_number += 1  # tmp round
        # Evaluation
        F_obj = []
        for i_eva, n in zip(Chromosome, range(len(Chromosome))):
            F_obj.append(abs(2 * i_eva[0] + 4 * i_eva[1] + 3 * i_eva[2] - 2 * i_eva[3] - 41))
            if F_obj[n] == 0:
                Best_Chromosome = copy.deepcopy(i_eva)
                break
        if min(F_obj) != 0:
            print("Round : {} Min : {} - Population : {}".format(Round_number, min(F_obj), Chromosome))
        else:
            print('\n')
            print("-"*40)
            temp_Round.append(Round_number)
            print("Round : {} Min : {} - Population : {}".format(Round_number, min(F_obj), Chromosome))
            print("Best Chromosome : ", Best_Chromosome)
            print("F_obj : ", min(F_obj))
            print("-"*40)
            print('\n')
            break

        # Selection
        Fitness_select = []
        Total_Fitness = 0
        Prob_select = []
        Cumulative = 0
        Prob_Cumulative = []
        for i_select in range(len(F_obj)):
            Fitness_select.append(round(1 / (1 + F_obj[i_select]), 4))
            Total_Fitness += Fitness_select[i_select]
        for i_prob in range(len(F_obj)):
            Prob_select.append(round(Fitness_select[i_prob] / Total_Fitness, 4))
            Cumulative += Prob_select[i_prob]
            Prob_Cumulative.append(round(Cumulative, 4))

        # gen R for new Chromosome
        R_newChr = genR(len(Chromosome))

        # Gen new Chromosome
        New_chromosome = []
        for R_round in range(len(Chromosome)):
            for C_check in range(len(Chromosome)):
                if R_newChr[R_round] <= Prob_Cumulative[C_check]:
                    New_chromosome.append(Chromosome[C_check])
                    break
        # gen R for Parent
        R_parent = genR(len(New_chromosome))
        # gen Parent
        crs_Rate = round(crsOver_rate / 100, 4)
        Parent = [New_chromosome[i_crs] for i_crs in range(len(New_chromosome)) if R_parent[i_crs] <= crs_Rate]
        Cut_Points = [rnd(1, 3) for _ in range(len(Parent))]
        Parent_Idx = [i_crs for i_crs in range(len(New_chromosome)) if R_parent[i_crs] <= crs_Rate]

        # #beforeCrossoverChromosome = copy.deepcopy(New_chromosome)
        # crossOver
        if len(Parent) >= 1:
            Parent_crs = copy.deepcopy(Parent)
            for n, cut_point in zip(range(len(Parent)), Cut_Points):
                del Parent_crs[n][cut_point:]
                if n != len(Parent) - 1:  # if it's not last chromosome
                    for index, val in enumerate(Parent[n + 1]):
                        if index >= cut_point:
                            Parent_crs[n].append(val)
                else:  # if it's last chromosome
                    for index, val in enumerate(Parent[0]):
                        if index >= cut_point:
                            Parent_crs[n].append(val)
            # assign parent chromosome back to New_Chromosome
            for lis, n in zip(Parent_Idx, range(len(Parent_Idx))):
                del New_chromosome[lis][:]
                for _, val in enumerate(Parent_crs[n]):
                    New_chromosome[lis].append(val)

            # #beforeMutationChromosome = copy.deepcopy(New_chromosome)
            # Mutation
            Permutation_rate = round(perMut_rate / 100, 4)
            Total_gen = len(New_chromosome) * len(New_chromosome[0])  # total len of gen
            Num_mutation = math.floor(Permutation_rate * Total_gen)
            PosChro = []  # Position in chromosome
            ValLis = []  # value of mutated
            PosLis = []  # Position of List(Chromosome)
            PosInLis = []  # Position in PosLis
            for n in range(Num_mutation):
                PosChro.append(rnd(0, Total_gen - 1))
                ValLis.append(rnd(1, 41))
                PosLis.append(PosChro[n] // 4)
                PosInLis.append(PosChro[n] % 4)
                New_chromosome[PosLis[n]].insert(PosInLis[n], ValLis[n])  # insert(inx, ele)
                del New_chromosome[PosLis[n]][PosInLis[n] + 1]
        Chromosome = copy.deepcopy(New_chromosome)


if __name__ == '__main__':
    gen_Algorithm(30, 20)  # crossOver_Rate, mutation_Rate
