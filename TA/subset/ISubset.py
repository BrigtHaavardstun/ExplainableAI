import abc


class ISubsetSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_next_subset(self, previus_score, previus_subset):
        """
        Returns the next subset from S such to be evaluated.
        """
        pass

    @abc.abstractmethod
    def load(self, all_data_zip, true_data_zip, false_data_zip):
        "test"
        pass
