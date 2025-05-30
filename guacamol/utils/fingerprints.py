from typing import Literal

from rdkit.Chem import AllChem, Mol
from rdkit.Chem.AtomPairs.Sheridan import GetBPFingerprint, GetBTFingerprint
from rdkit.Chem.Pharm2D import Generate, Gobbi_Pharm2D
from rdkit.DataStructs import (
    ExplicitBitVect,
    IntSparseIntVect,
    LongSparseIntVect,
    SparseBitVect,
    UIntSparseIntVect,
)
from typing_extensions import TypeAlias

FpT: TypeAlias = (
    "IntSparseIntVect | SparseBitVect | LongSparseIntVect | ExplicitBitVect | UIntSparseIntVect"
)
FpNameT = Literal["AP", "PHCO", "BPF", "BTF", "PATH", "ECFP4", "ECFP6", "FCFP4", "FCFP6"]


class _FingerprintCalculator:
    """
    Calculate the fingerprint while avoiding a series of if-else.
    See recipe 8.21 of the book "Python Cookbook".

    To support a new type of fingerprint, just add a function "get_fpname(self, mol)".
    """

    def get_fingerprint(self, mol: Mol, fp_type: FpNameT) -> FpT:
        method_name = "get_" + fp_type
        method = getattr(self, method_name)
        if method is None:
            raise Exception(f"{fp_type} is not a supported fingerprint type.")
        return method(mol)

    def get_AP(self, mol: Mol) -> IntSparseIntVect:
        return AllChem.GetAtomPairFingerprint(mol, maxLength=10)

    def get_PHCO(self, mol: Mol) -> SparseBitVect:
        return Generate.Gen2DFingerprint(mol, Gobbi_Pharm2D.factory)

    def get_BPF(self, mol: Mol) -> IntSparseIntVect:
        return GetBPFingerprint(mol)

    def get_BTF(self, mol: Mol) -> LongSparseIntVect:
        return GetBTFingerprint(mol)

    def get_PATH(self, mol: Mol) -> ExplicitBitVect:
        return AllChem.RDKFingerprint(mol)

    def get_ECFP4(self, mol: Mol) -> UIntSparseIntVect:
        return AllChem.GetMorganFingerprint(mol, 2)

    def get_ECFP6(self, mol: Mol) -> UIntSparseIntVect:
        return AllChem.GetMorganFingerprint(mol, 3)

    def get_FCFP4(self, mol: Mol) -> UIntSparseIntVect:
        return AllChem.GetMorganFingerprint(mol, 2, useFeatures=True)

    def get_FCFP6(self, mol: Mol) -> UIntSparseIntVect:
        return AllChem.GetMorganFingerprint(mol, 3, useFeatures=True)


def get_fingerprint(mol: Mol, fp_type: FpNameT) -> FpT:
    return _FingerprintCalculator().get_fingerprint(mol=mol, fp_type=fp_type)
