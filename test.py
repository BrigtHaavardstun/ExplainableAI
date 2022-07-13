

def get_teaching_sets():
    all_text_lines = ""
    with open("run_result/best/over_all_best.csv", "r") as f:
        all_text_lines = f.read().split("\n")

    map_to_fix = {}
    for i, row in enumerate(all_text_lines[1:]):
        labels = row.split(",")[8].split("-")
        predictions = row.split(",")[9].split("-")
        text = "{"
        if labels[0] == "":
            labels[0] = "#"
        text += f"({labels[0]},{predictions[0]})"
        for j in range(1, len(labels)):
            if labels[j] == "":
                labels[j] = "#"
            text += f",({labels[j]},{predictions[j]})"
        text += "}"
        if text not in map_to_fix:
            map_to_fix[text] = []
        map_to_fix[text].append(i)

    for text in map_to_fix.keys():
        print(text, map_to_fix[text])


def get_delta_score():
    all_text_lines = ""
    with open("run_result/best/over_all_best.csv", "r") as f:
        all_text_lines = f.read().split("\n")

    for i, row in enumerate(all_text_lines[1:]):
        print(row.split(",")[6].replace(".", ","),  end=" ")


def get_lambda_score():
    all_text_lines = ""
    with open("run_result/best/over_all_best.csv", "r") as f:
        all_text_lines = f.read().split("\n")

    for i, row in enumerate(all_text_lines[1:]):
        print(row.split(",")[5].replace(".", ","),  end=" ")


get_lambda_score()

text = """2,224585388
2,840944974
2,389495519
0,554591995
1.432568252
1.172835643
0.814534323
1.140433432
1.532247415
1.052735297
1.24067945
0.497421739
1.129504191
0.43370134
0.255907915
0.00056877
"""
for line in text.split():
    print(line.replace(".", ","), end=" ")
