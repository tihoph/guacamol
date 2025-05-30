from collections.abc import Sequence

from guacamol.distribution_matching_generator import DistributionMatchingGenerator


class MockGenerator(DistributionMatchingGenerator):
    """
    Mock generator that returns pre-defined molecules,
    possibly split in several calls
    """

    def __init__(self, molecules: Sequence[str]) -> None:
        self.molecules = molecules
        self.cursor = 0

    def generate(self, number_samples: int) -> list[str]:
        end = self.cursor + number_samples

        sampled_molecules = self.molecules[self.cursor : end]
        self.cursor = end
        return list(sampled_molecules)
