import random
Roulette = [1, 2, 3]
PROBABILITY = 1/len(Roulette)
########
# Resumo do código
# Ele calcula de jeito bruto a probabilidade de todas as sequências e as funções apenas filtram o necessário
# Todo o código nesse caso baseado em objetos
########

# Perdão para quem queria um código que fosse matematicamente correto só que domingão não é dia de pensar nisso não
def get_min(array):
    min_value = None
    for i in array:
        if min_value is None:
            min_value = len(i)
        if len(i) < min_value:
            min_value = len(i)
    return min_value

def sum_array(array):
    total = 0
    for i in array:
        total += i
    return total

class Table():
    def __init__(self, squares = 3):
        self.squares = squares
        if self.squares < 3:
            self.squares = 3
    
    def return_squares(self):
        return self.squares

class Player():
    def __init__(self, position: int, table:Table):
        self.position = position
        self.table = table
        self.won = False
       
    def calculate_all_steps_possible(self, max_steps = 3, max_sequences = 5, can_reset = True, verbose = False, auto_break = True, max_number_attempts = 100):
        sequences = []
        max_number_attempts_counter = 0
        if verbose: print("Aperte Ctrl+C para parar a execução e retornar as sequências encontradas até o momento.")
        try:
            sequence = []
            while self.won == False:
                rand = random.choice(Roulette)
                sequence.append(rand)
                self.position += rand
                if self.position < 0:
                    self.position = 0
                if self.position > self.table.return_squares():
                    self.position = 0
                if self.position == self.table.return_squares():
                    if sequence not in sequences:
                        if verbose and can_reset: print(f"Sequencia nova: {sequence}")
                        if can_reset:                
                            sequences.append(sequence)
                            sequence = []
                            self.position = 0
                        else:
                            if sum_array(sequence) > self.table.return_squares():
                                max_number_attempts_counter += 1
                                sequence = []
                                self.position = 0
                            else:
                                if verbose: print(f"Sequencia sem reset: {sequence}")
                                sequences.append(sequence)
                                sequence = []
                                self.position = 0
                    else:
                        max_number_attempts_counter += 1
                        sequence = []
                        self.position = 0
                if sequence.__len__() > max_steps:
                    sequence = []
                    self.position = 0
                if sequences.__len__() >= max_sequences:
                    return sequences
                if auto_break and max_number_attempts_counter >= max_number_attempts:
                    return sequences
        except KeyboardInterrupt:
            return sequences
    
    def calculate_min_steps(self, max_steps = 40, max_sequences = 400,can_reset = False, verbose = False):
        if verbose:print("Calculando quantidade mínima de movimentos...")
        all_sequences = self.calculate_all_steps_possible(max_steps, max_sequences, can_reset, verbose)
        min_sequence = get_min(all_sequences)
        return min_sequence

    def calculate_steps_without_reset(self, max_steps = 40, max_sequences = 400, verbose = False):
        if verbose:print("Calculando movimentos sem reset...")
        return self.calculate_all_steps_possible(max_steps, max_sequences, can_reset=False, verbose=verbose)

    def calculate_probability_for_best_move(self, verbose = False):
        if verbose:print("Calculando probabilidade do melhor movimento em sequência...")
        calculate_min = self.calculate_min_steps(can_reset=False, verbose=verbose)
        probability = PROBABILITY ** calculate_min
        if verbose:
            print(f"Precisa pular quantas casas para ganhar: {calculate_min}")
            print(f"Probabilidade do melhor movimento: {probability}")
            print(f"Em porcentagem: {round(probability * 100)}%")
        return probability

if __name__ == "__main__":
    print("Calculo de probabilidade com table de 3 CASAS.")
    table = Table(3)
    player = Player(0, table)
    min_steps = player.calculate_min_steps(verbose=False)
    prob = player.calculate_probability_for_best_move(verbose=False)
    print(f"Menor quantidade de passos para ganhar: {min_steps}")
    print(f"Probabilidade do melhor movimento: {prob} ({round(prob * 100)}%)")
    sequences_without_reset = player.calculate_steps_without_reset(verbose=False)
    print(f"Foram encontradas {sequences_without_reset.__len__()} sequências sem reset:")
    print("////////////////////////////////")
    
    print("Calculo de probabilidade com table de 14 CASAS.")
    table = Table(14)
    player = Player(0, table)
    min_steps = player.calculate_min_steps(verbose=False)
    prob = player.calculate_probability_for_best_move(verbose=False)
    print(f"Menor quantidade de passos para ganhar: {min_steps}")
    print(f"Probabilidade do melhor movimento: {prob} ({round(prob * 100)}%)")
    sequences_without_reset = player.calculate_steps_without_reset(verbose=False)
    print(f"Foram encontradas {sequences_without_reset.__len__()} sequências sem reset:")
