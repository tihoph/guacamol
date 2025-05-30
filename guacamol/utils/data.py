from __future__ import annotations

import os
import sys
import time
from typing import TYPE_CHECKING, Any
from urllib.request import urlretrieve

import numpy as np
from tqdm import tqdm

if TYPE_CHECKING:
    from collections.abc import Sequence


def remove_duplicates(list_with_duplicates: Sequence[str]) -> list[str]:
    """
    Removes the duplicates and keeps the ordering of the original list.
    For duplicates, the first occurrence is kept and the later occurrences are ignored.

    Args:
        list_with_duplicates: list that possibly contains duplicates

    Returns:
        A list with no duplicates.
    """

    unique_set: set[str] = set()
    unique_list = []
    for element in list_with_duplicates:
        if element not in unique_set:
            unique_set.add(element)
            unique_list.append(element)

    return unique_list


def get_random_subset(
    dataset: Sequence[str],
    subset_size: int,
    seed: int | None = None,
) -> list[str]:
    """
    Get a random subset of some dataset.

    For reproducibility, the random number generator seed can be specified.
    Nevertheless, the state of the random number generator is restored to avoid side effects.

    Args:
        dataset: full set to select a subset from
        subset_size: target size of the subset
        seed: random number generator seed. Defaults to not setting the seed.

    Returns:
        subset of the original dataset as a list
    """
    if len(dataset) < subset_size:
        raise Exception(
            f"The dataset to extract a subset from is too small: {len(dataset)} < {subset_size}",
        )

    # save random number generator state
    rng_state = np.random.get_state()

    if seed is not None:
        # extract a subset (for a given training set, the subset will always be identical).
        np.random.seed(seed)

    subset = np.random.choice(dataset, subset_size, replace=False)

    if seed is not None:
        # reset random number generator state, only if needed
        np.random.set_state(rng_state)

    return list(subset)


def download_if_not_present(filename: str, uri: str) -> None:
    """
    Download a file from a URI if it doesn't already exist.
    """
    if os.path.isfile(filename):
        print("{} already downloaded, reusing.".format(filename))
    else:
        with open(filename, "wb") as fd:
            print("Starting {} download from {}...".format(filename, uri))
            with ProgressBarUpTo(unit="B", unit_scale=True, unit_divisor=1024, miniters=1) as t:
                urlretrieve(uri, fd.name, reporthook=t.update_to)  # noqa: S310
            print("Finished {} download.".format(filename))


class ProgressBar(tqdm):
    """
    Create a version of TQDM that notices whether it is going to the output or a file.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Overwrite TQDM and detect if output is a file or not."""
        # See if output is a terminal, set to updates every 30 seconds
        if not sys.stdout.isatty():
            kwargs["mininterval"] = 30.0
            kwargs["maxinterval"] = 30.0
        super().__init__(*args, **kwargs)


class ProgressBarUpTo(ProgressBar):
    """
    Fancy Progress Bar that accepts a position not a delta.
    """

    def update_to(self, b: int = 1, bsize: int = 1, tsize: int | None = None) -> None:
        """
        Update to a specified position.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


def get_time_string() -> str:
    lt = time.localtime()
    return "%04d%02d%02d-%02d%02d" % (
        lt.tm_year,
        lt.tm_mon,
        lt.tm_mday,
        lt.tm_hour,
        lt.tm_min,
    )
