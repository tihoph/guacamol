from rdkit import Chem

from guacamol.utils.descriptors import AtomCounter, num_atoms


def test_num_atoms() -> None:
    smiles = "CCOC(CCC)"
    mol = Chem.MolFromSmiles(smiles)
    assert num_atoms(mol) == 21


def test_num_atoms_does_not_change_mol_instance() -> None:
    smiles = "CCOC(CCC)"
    mol = Chem.MolFromSmiles(smiles)

    assert mol.GetNumAtoms() == 7
    num_atoms(mol)
    assert mol.GetNumAtoms() == 7


def test_count_c_atoms() -> None:
    smiles = "CCOC(CCC)"
    mol = Chem.MolFromSmiles(smiles)
    assert AtomCounter("C")(mol) == 6


def test_count_h_atoms() -> None:
    smiles = "CCOC(CCC)"
    mol = Chem.MolFromSmiles(smiles)
    assert AtomCounter("H")(mol) == 14


def test_count_h_atoms_does_not_change_mol_instance() -> None:
    smiles = "CCOC(CCC)"
    mol = Chem.MolFromSmiles(smiles)

    assert mol.GetNumAtoms() == 7
    AtomCounter("H")(mol)
    assert mol.GetNumAtoms() == 7
