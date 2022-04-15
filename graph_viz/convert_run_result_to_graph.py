import pandas as pd
import matplotlib.pyplot as plt


def run(path_to_csv_file):
    df = pd.read_csv(path_to_csv_file)
    make_graph_on_sub_set_selector(df)


def make_graph_on_sub_set_selector(df):
    sub_set_selectors_to_data = {}
    for itr, complexity, compatibility, sub_set_selctor in zip(df.sample_attemps, df.compatibility, df.complexity, df.subset_selectors):
        if sub_set_selctor not in sub_set_selectors_to_data:
            sub_set_selectors_to_data[sub_set_selctor] = [
                (itr, complexity, compatibility)]
        else:
            sub_set_selectors_to_data[sub_set_selctor].append(
                (itr, complexity, compatibility))

    for sub_set_selctor in sub_set_selectors_to_data.keys():
        print(f"{'#'*10}{sub_set_selctor}{'#'*10}")
        complexity_itterations = {}  # [(complexity_score, itterations)]
        compatibility_itterations = {}  # [(complexity_score, itterations)]

        # Get all in the same
        for itr, compatibility, complexity in sub_set_selectors_to_data[sub_set_selctor]:
            if itr in complexity_itterations:
                complexity_itterations[itr].append(complexity)
            else:
                complexity_itterations[itr] = [complexity]

            if itr in compatibility_itterations:
                compatibility_itterations[itr].append(compatibility)
            else:
                compatibility_itterations[itr] = [compatibility]

        # Calulate average
        for itr in complexity_itterations.keys():
            compatibility_itterations[itr] = sum(
                compatibility_itterations[itr]) / len(compatibility_itterations[itr])
            complexity_itterations[itr] = sum(
                complexity_itterations[itr]) / len(complexity_itterations[itr])

        x = []
        complexity_y = []
        compatibility_y = []
        for itr in sorted(complexity_itterations.keys()):
            print(
                f"itr: {itr}, complexity: {complexity_itterations[itr]}, compatibility: {compatibility_itterations[itr]}")
            x.append(itr)
            complexity_y.append(complexity_itterations[itr])
            compatibility_y.append(compatibility_itterations[itr])

        plt.plot(x, compatibility_y, label=f"{sub_set_selctor}-compat")
        #plt.plot(x, complexity_y, label=f"{sub_set_selctor}-complex")
    plt.legend(loc="upper left")
    plt.ylim(0, 2.0)
    plt.show()
