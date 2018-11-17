from itertools import groupby
from typing import List, Tuple

from sympy import Matrix


class Face:
    """ this class is used for typing clarity and ordering of inputs"""

    def __init__(self, face: List[int]):
        self.face = sorted(face)

    def __len__(self):
        return len(self.face)

    def dim(self):
        return len(self.face) - 1

    def get_sub_faces(self) -> List['Face']:
        out_faces = []

        if self.dim() > 0:
            for i in range(len(self.face)):
                out_face = self.face.copy()
                out_face.pop(i)
                out_faces.append(Face(out_face))

        return out_faces

    def get_image(self) -> List[Tuple[int, 'Face']]:
        sub_faces = self.get_sub_faces()
        power = 1
        output = []
        for face in sub_faces:
            output.append((power, face))
            power *= -1

        return output

    def standard_basis_index(self, max_vertex: int) -> int:
        index = 0
        power = 1
        for value in self.face:
            index += (value - 1) * power
            power *= max_vertex

        return index

    def representation_in_standard_basis(self, max_vertex: int):
        representation = [0] * pow(max_vertex, len(self.face))
        index = self.standard_basis_index(max_vertex=max_vertex)
        representation[index] = 1
        return representation


def are_same_face(face1: Face, face2: Face) -> bool:
    # If faces have different lengths they are different.
    if face1.dim() != face2.dim():
        return False

    # Iterate over both faces and check if they are the same element-wise.
    for index1, index2 in zip(face1.face, face2.face):
        if index1 != index2:
            return False

    # If we have reached this point then they are the same face.
    return True


def get_all_indexes(list_vectors: List[List[Tuple[int, Face]]], max_vertex: int) -> List[int]:
    indexes = []
    for vector in list_vectors:
        indexes.extend([face.standard_basis_index(max_vertex=max_vertex) for _, face in vector])
    return sorted(list(set(indexes)))


def get_conversion_matrix(list_vectors: List[List[Tuple[int, Face]]],
                          all_indexes: List[int],
                          max_vertex: int) -> Matrix:
    conversion_matrix = []
    for vector in list_vectors:
        column = [0] * len(all_indexes)
        for factor, face in vector:
            index = face.standard_basis_index(max_vertex=max_vertex)
            index = all_indexes.index(index)
            column[index] = factor

        conversion_matrix.append(column)

    return Matrix(conversion_matrix).transpose()


class Basis:
    def __init__(self, basis: List[List[Tuple[int, Face]]], max_vertex: int):
        self.basis = basis
        self.max_vertex = max_vertex

        self._basis_indexes = get_all_indexes(list_vectors=basis, max_vertex=max_vertex)

        self._conversion_matrix = get_conversion_matrix(list_vectors=basis,
                                                        all_indexes=self._basis_indexes,
                                                        max_vertex=max_vertex)

        self._reduced_basis_indexes = self._basis_indexes
        self._reduced_conversion_matrix = self._conversion_matrix
        for i in range(self._conversion_matrix.rows - self._conversion_matrix.cols):
            candidate_matrix = self._conversion_matrix[i: i + self._conversion_matrix.cols, :]
            if candidate_matrix.det() != 0:
                self._reduced_basis_indexes = self._basis_indexes[i: i + self._conversion_matrix.cols]
                self._reduced_conversion_matrix = candidate_matrix
                break

        self._standard_to_basis_conversion = self._reduced_conversion_matrix.inv()

    def representation_on_basis(self, chain: List[Tuple[int, Face]]) -> Matrix:
        chain = [(factor, face.standard_basis_index(self.max_vertex)) for factor, face in chain]
        chain = [(factor, index) for factor, index in chain if index in self._reduced_basis_indexes]

        standard_basis_chain = [0] * len(self._reduced_basis_indexes)
        for coefficient, index in chain:
            index = self._reduced_basis_indexes.index(index)
            standard_basis_chain[index] = coefficient

        standard_basis_chain = Matrix([standard_basis_chain]).transpose()
        return self._standard_to_basis_conversion * standard_basis_chain

    def dim(self) -> int:
        return len(self.basis)


class Group:
    def __init__(self, group: List[int]):
        self.group = sorted([value for value in group if value != 1])

    def __str__(self):
        # If the list is empty then the homology is 0.
        if len(self.group) == 0:
            return '0'

        # We sort the list and group the values to obtain a more readable result.
        group = sorted(self.group)
        group = [(key, len(list(group))) for key, group in groupby(group)]

        # Initialize output and, for every element of the input group we add to the output the corresponding
        output = ''
        for characteristic, index in group:
            # Print the group.
            if characteristic == 0:
                output += 'ZX'
            else:
                output += 'Z/({})X'.format(characteristic)

            # Print its multiplicity.
            if index > 1:
                output = output[:-1] + '^{}'.format(index)

        # Remove last element from output string and return the result.
        return output[:-1]
