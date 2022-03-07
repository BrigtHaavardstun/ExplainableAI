from utils.common import get_all_permutations
all_possibilites = []
choices = get_all_permutations()
for first in choices:
    for second in choices:
        for third in choices:
            for fourth in choices:
                current = ",".join(sorted([first, second, third, fourth]))
                if first == second or first == third or first == fourth:
                    continue
                if second == third or second == fourth:
                    continue
                if third == fourth:
                    continue
                if current not in all_possibilites:
                    all_possibilites.append(current)
print(len(all_possibilites))
with open("correct.txt", "w") as f:
    f.write("\n".join(sorted(all_possibilites)))
