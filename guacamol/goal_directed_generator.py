from __future__ import annotations

from abc import ABCMeta, abstractmethod

from guacamol.scoring_function import ScoringFunction
from collections.abc import Sequence


class GoalDirectedGenerator(metaclass=ABCMeta):
    """
    Interface for goal-directed molecule generators.
    """

    @abstractmethod
    def generate_optimized_molecules(
        self,
        scoring_function: ScoringFunction,
        number_molecules: int,
        starting_population: Sequence[str] | None = None,
    ) -> list[str]:
        """
        Given an objective function, generate molecules that score as high as possible.

        Args:
            scoring_function: scoring function
            number_molecules: number of molecules to generate
            starting_population: molecules to start the optimization from (optional)

        Returns:
            A list of SMILES strings for the generated molecules.
        """
