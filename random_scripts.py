from run_result import count_apperance
from models.trainModel import load_model
from utils.dataset import load_dataset
from time import perf_counter
import pandas as pd
from graph_viz.convert_run_result_to_graph import run as graph_viz_run

from utils.global_props import score_function


# count_apperance.main()

# graph_viz_run("run_result/best/over_all_best.csv")

def find_most_common_sample(teaching_set_size, target_attempts):
    path_to_csv_file = f"run_result/run_result{teaching_set_size}.csv"
    df = pd.read_csv(path_to_csv_file)
    all_teaching_sets = {}

    all_labels = [df[e].map(str)
                  for e in list(df) if "label" in e]

    all_labels_summed = all_labels[0]
    for label in all_labels[1:]:
        all_labels_summed = all_labels_summed.map(str) + "," + label.map(str)

    # new stuff
    all_labels_post_sum = []
    for label in all_labels_summed.tolist():
        label = label.replace("nan", "#")
        all_labels_post_sum.append("-".join(label.split(",")))
    all_teaching_set = all_labels_post_sum

    all_predictions = [df[e].map(str)
                       for e in list(df) if "prediction" in e]

    all_preds_summed = all_predictions[0]
    for preds in all_predictions[1:]:
        all_preds_summed = all_preds_summed.map(str) + "," + preds.map(str)

    all_teaching_set = all_labels_post_sum + \
        all_preds_summed.map(lambda x: "\n" + str(x))
    all_teaching_set = all_teaching_set.tolist()

    sub_set_selctor_map = {}
    teaching_set_to_score = {}

    for attemps, teaching_set, sub_set_selctor, compatibility, complexity in zip(df.sample_attemps, all_teaching_set, df.subset_selectors, df.compatibility, df.complexity):
        teaching_set_to_score[teaching_set] = score_function(
            compatibility=compatibility, complexity=complexity)
        if sub_set_selctor not in sub_set_selctor_map:
            sub_set_selctor_map[sub_set_selctor] = {}
        if target_attempts == attemps:
            if teaching_set in sub_set_selctor_map[sub_set_selctor]:
                sub_set_selctor_map[sub_set_selctor][teaching_set] += 1
            else:
                sub_set_selctor_map[sub_set_selctor][teaching_set] = 1

    for sub_set_selector in sub_set_selctor_map.keys():
        curr_map = sub_set_selctor_map[sub_set_selector]
        most_popular_teaching_sets = max(
            curr_map.keys(), key=lambda x: curr_map[x])
        print(
            f"{sub_set_selector}:\n{most_popular_teaching_sets}\n{curr_map[most_popular_teaching_sets]}/{sum(curr_map.values())} ")


def get_most_common_sample(target_attempts):
    for i in range(1, 9):
        print(f"{'#'*20}{i}{'#'*20}")
        find_most_common_sample(i, target_attempts=target_attempts)


if __name__ == "__main__":
    # graph_viz_run("run_result/best/over_all_best.csv")
    get_most_common_sample(target_attempts=60)
