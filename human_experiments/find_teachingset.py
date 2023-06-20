import random
from random import randint, shuffle, choice
from utils.common import one_hot_to_number
from utils.dataset import load_dataset
from utils.common import remove_digit_from_labels, one_hot_to_number
from PIL import Image


def get_images_matching_teaching_set(teaching_set, ai, verbose=False, seed=420):
    rnd = random.Random(seed)
    images = []
    # X, Y, labels = load_dataset()

    found = []
    title = []
    for example in teaching_set:
        example_label, value = example
        print("label: ", example_label)
        found = False
        X, Y, labels = load_dataset()
        test_values = (list(range(len(X)-1, 0, -1)))
        rnd = random.Random(seed)
        if example_label != "":
            # We want each label from the same seed to be identical
            rnd = random.Random(seed + int(example_label, 32))
        rnd.shuffle(test_values)
        for i in test_values:
            corr_label = "".join(remove_digit_from_labels(labels[i]))

            if corr_label == example_label:
                if one_hot_to_number(ai.predict(X[i])) == value:
                    images.append(Image.fromarray(X[i]))
                    title.append(value)
                    found = True
                    break
        if not found:
            print("Could not find a data instance with the combination of: ",
                  example_label, value)
    if verbose:
        for img, title in zip(images, title):
            img.show(title=title)
    return images


def generate_random_teaching_set_of_size_k(k, ai):
    X, Y, labels = load_dataset()
    random_combo = list(zip(X, labels))
    print("Should not be used?")
    shuffle(random_combo)

    img_to_show = []
    ai_values = []
    letters = []
    while len(letters) < k:
        x, l = choice(random_combo)
        l = "".join(remove_digit_from_labels(l))
        if l not in letters:
            letters.append(l)
            img_to_show.append(Image.fromarray(x))
            ai_values.append(one_hot_to_number(ai.predict(x)))
    for i in range(len(img_to_show)):
        print(letters[i], ai_values[i])
        img_to_show[i].show()
