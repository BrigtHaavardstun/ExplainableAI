
from TA.delta.sumOfExamples import SumOfExamples
from TA.delta.maxExample import MaxExample
from TA.delta.minExample import MinExample
from TA.delta.squaredSum import SquaredSum
from TA.delta.absExample import AbsExample
from TA.delta.Cardinality import Cardinality
from TA.delta.Chunking import Chunking


def main():
    deltas = [SumOfExamples(), MaxExample(), MinExample(), SquaredSum(),
              AbsExample(), Chunking(), Cardinality()]
    deltas = sorted([str(delta) for delta in deltas])

    file = "run_result/best/over_all_best.csv"
    total_tally = {}
    for delta in deltas:
        total_tally[delta] = {}
    with open(file, "r") as f:
        text = f.read()
        for delta in deltas:
            total_tally[delta] = text.count(delta)

    for delta in deltas:
        print(delta, total_tally[delta])


if __name__ == "__main__":
    main()
