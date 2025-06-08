"""Parallelize with joblib or threading with optional progress bar."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, TypeVar

import joblib
from tqdm import tqdm
from typing_extensions import TypeVarTuple, Unpack

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

T = TypeVar("T")
TupT = TypeVarTuple("TupT")


def parallelize(
    func: Callable[[Unpack[TupT]], T],
    jobs_args: Sequence[tuple[Unpack[TupT]]],
    n_jobs: int = 8,
    desc: str | None = None,
    leave: bool = True,
    verbose: int = 0,
) -> list[T]:
    """Parallelize a function over multiple processes.

    Args:
        func: Function to parallelize. Only positional arguments are supported.
            The function must be pickleable.
        jobs_args: Arguments for the function.
            Each tuple corresponds to a single call of the function.
        n_jobs: Number of processes to use.
            Will be overwritten by "GUACAMOL_PROC" environment variable if set.
        desc: Description of the task.
        leave: Whether to leave the progress bar after the task is done.
        verbose: Verbosity level.

    Returns:
        List of results from the function in order of inputs.
    """
    env_jobs = os.getenv("GUACAMOL_PROC")
    n_jobs = int(env_jobs) if env_jobs else n_jobs
    jobs = [joblib.delayed(func)(*args) for args in jobs_args]

    with joblib.Parallel(n_jobs=n_jobs, return_as="generator") as p:
        return list(tqdm(p(jobs), desc=desc, total=len(jobs), leave=leave, disable=verbose == 0))
