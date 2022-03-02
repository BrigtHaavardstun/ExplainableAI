
from models.abstract_model import AbstractModel


class LoadModel(AbstractModel):
    def __init__(self, model, name: str = "Defualt", verbose: bool = True):
        super(LoadModel, self).__init__(
            model=model, name=name, verbose=verbose)

    def _set_layers(self):
        """
        This has to be done in sub class. However, since we only load an existing model, we don't need to have it.
        """
        return None
