from numpy import False_
from generator import four_places_image, pastingImages
from data import convert_images_to_bitmask_par, generateLabels


def main(fixedSquare: bool = True, verbose: bool = True, rotation: bool = False, scale: bool = False):

    if fixedSquare:
        if verbose:
            print("Generating images using four_places routine...")

        four_places_image.run(rotation=rotation, scale=scale, verbose=False)
    else:
        if verbose:
            print("Generating images using random placement routine...")
        pastingImages.run()

    if verbose:
        print("Converting images to bitmasks")
    convert_images_to_bitmask_par.run()

    if verbose:
        # TODO: Add dispaly of boolean function. Use custom boolExpr
        print("Generating labels from boolean function...")

    generateLabels.run()


if __name__ == '__main__':
    main(fixedSquare=True, rotation=True, scale=True)
