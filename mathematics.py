import math
from typing import List, Tuple, Optional

from sympy import Matrix

from utils import Face, Group, are_same_face, Basis, get_all_indexes, get_conversion_matrix


def get_homology_groups(faces: List[Face]) -> List[Group]:
    max_vertex = get_max_vertex(faces=faces)

    all_faces = get_all_faces(faces=faces)

    simplicial_complex = gather_faces_by_length(all_faces)

    kernels_basis = get_kernels_basis(simplicial_complex=simplicial_complex, max_vertex=max_vertex)
    images_basis = get_images(simplicial_complex=simplicial_complex)
    connection_matrices = get_connection_matrices(kernels_basis=kernels_basis,
                                                  images=images_basis)

    kernel_dims = [kernel.dim() for kernel in kernels_basis]
    diagonals = diagonalize_matrices(matrices=connection_matrices, kernel_dims=kernel_dims)
    return [Group(diagonal) for diagonal in diagonals]


def get_max_vertex(faces: List[Face]) -> int:
    max_vertex = 1
    for face in faces:
        max_face = max(face.face)
        if max_face > max_vertex:
            max_vertex = max_face

    return max_vertex


def get_all_faces(faces: List[Face]) -> List[Face]:
    # Initialize output faces.
    out_faces = []

    # The output faces must contain the faces in the input list.
    out_faces.extend(faces)

    # For every face in the input list the output must contain all its sub_faces.
    # If the input list is empty this loop is never entered.
    for face in faces:
        # Get all sub-faces.
        out_faces.extend(get_all_faces(face.get_sub_faces()))

    return out_faces


def gather_faces_by_length(faces: List[Face]) -> List[List[Face]]:
    faces = sorted(faces, key=lambda x: x.dim())
    out_faces = []
    i = 0
    while len(faces) > 0:
        # Initialize set of faces with the current length i.
        level_faces = []

        # Get all faces with dimension i and remove them from the list of faces.
        j = 0
        while j < len(faces):
            if faces[j].dim() == i:
                level_faces.append(faces[j])
                faces.pop(j)
                j -= 1
            j += 1

        # Make sure all faces in this level are different.
        level_faces = remove_equal_faces(level_faces)

        out_faces.append(level_faces)
        i += 1

    return out_faces


def remove_equal_faces(face_list: List[Face]) -> List[Face]:
    out_list = []

    while len(face_list) > 0:
        # Get a face from the list.
        new_face = face_list.pop()
        out_list.append(new_face)

        # Remove all faces equal to the just obtained face.
        i = 0
        while i < len(face_list):
            if are_same_face(new_face, face_list[i]):
                face_list.pop(i)
                i -= 1
            i += 1

    return out_list


def get_kernels_basis(simplicial_complex: List[List[Face]], max_vertex: int) -> List[Basis]:
    if len(simplicial_complex) == 0:
        return []

    simplicial_complex = simplicial_complex.copy()
    level_0 = [[(1, face)] for face in simplicial_complex.pop(0)]
    output = [Basis(level_0, max_vertex=max_vertex)]

    for level in simplicial_complex:
        output.append(get_kernel_basis(simplicial_level=level, max_vertex=max_vertex))

    return output


def get_kernel_basis(simplicial_level: List[Face], max_vertex: int) -> Basis:
    simplicial_level_images = [face.get_image() for face in simplicial_level]
    all_indexes = get_all_indexes(list_vectors=simplicial_level_images,
                                  max_vertex=max_vertex)
    matrix = get_conversion_matrix(list_vectors=simplicial_level_images,
                                   all_indexes=all_indexes,
                                   max_vertex=max_vertex)
    kernel = matrix.nullspace()
    kernel = [list(vector) for vector in kernel]

    basis = [[(coefficient, face) for coefficient, face in zip(vector, simplicial_level)] for vector in kernel]
    basis = Basis(basis=basis, max_vertex=max_vertex)

    return basis


def get_images(simplicial_complex: List[List[Face]]) -> List[List[List[Tuple[int, Face]]]]:
    if len(simplicial_complex) == 0:
        return []

    simplicial_complex = simplicial_complex.copy()
    simplicial_complex.pop(0)

    output = []
    for level in simplicial_complex:
        output.append([face.get_image() for face in level])

    output.append([])

    return output


def get_connection_matrices(kernels_basis: List[Basis],
                            images: List[List[List[Tuple[int, Face]]]]) -> List[Matrix]:
    output = []
    for kernel, level_images in zip(kernels_basis, images):
        connection_matrix = []
        for image in level_images:
            connection_matrix.append(list(kernel.representation_on_basis(chain=image)))
        output.append(Matrix(connection_matrix))

    return output


def diagonalize_matrices(matrices: List[Matrix], kernel_dims: List[int]) -> List[List[int]]:
    return [diagonalize_matrix(matrix, kernel_dim) for matrix, kernel_dim in zip(matrices, kernel_dims)]


def diagonalize_matrix(matrix: Matrix, kernel_dim: int, _recurrent: Optional[List[int]] = None) -> List[int]:
    if _recurrent is None:
        _recurrent = []

    matrix_dim = min(matrix.rows, matrix.cols)
    if matrix_dim == 0:
        # We add all non considered dimensions.
        output = _recurrent + [0]*(kernel_dim - len(_recurrent))
        return output

    # Make sure first element of each row is positive
    def process_matrix(m: Matrix) -> Matrix:
        out_matrix = []
        for i in range(m.rows):
            processed_row = matrix.row(i)
            if processed_row[0] < 0:
                processed_row = -processed_row

            out_matrix.append(list(processed_row))
        return Matrix(out_matrix)

    matrix = process_matrix(matrix).transpose()
    matrix = process_matrix(matrix)

    processed_matrix, value = reduction_on_first_element(matrix)

    _recurrent.append(value)

    return diagonalize_matrix(matrix=processed_matrix, kernel_dim=kernel_dim, _recurrent=_recurrent)


def reduction_on_first_element(matrix: Matrix) -> Tuple[Matrix, int]:
    is_reduced = True
    for i in range(1, matrix.cols):
        if matrix[0, i] != 0:
            is_reduced = False
            break

    if is_reduced:
        for i in range(1, matrix.rows):
            if matrix[i, 0] != 0:
                is_reduced = False
                break

    # If matrix is reduced we end here.
    if is_reduced:
        return matrix[1:, 1:], matrix[0, 0]

    # Iterate over rows and columns to obtain the smallest positive value in the first row and column
    min_index = (0, 0)
    smallest_value = matrix[min_index[0], min_index[1]]

    for i in range(1, matrix.cols):
        candidate = matrix[0, i]
        # If smallest value is 0 we have to perform a permutation.
        if 0 < candidate < smallest_value or smallest_value == 0:
            smallest_value = candidate
            min_index = (0, i)

    for i in range(1, matrix.rows):
        candidate = matrix[i, 0]
        # If smallest value is 0 we have to perform a permutation.
        if 0 < candidate < smallest_value or smallest_value == 0:
            smallest_value = candidate
            min_index = (i, 0)

    # place the smallest value in first place.
    if min_index[1] > 0:
        min_index = min_index[1]
        matrix = matrix.transpose()
    else:
        min_index = min_index[0]

    permutation = [i for i in range(matrix.rows)]
    permutation[0] = min_index
    permutation[min_index] = 0
    pre_processed_matrix = []

    for index in permutation:
        pre_processed_matrix.append(matrix.row(index))

    pre_processed_matrix = Matrix(pre_processed_matrix)
    row_reduced_matrix = row_reduce(pre_processed_matrix)
    processed_matrix = col_reduce(row_reduced_matrix)

    return reduction_on_first_element(processed_matrix)


def row_reduce(matrix: Matrix) -> Matrix:
    # Iterate over rows and columns performing reduction.
    first_row = matrix.row(0)
    min_value = first_row[0]
    reduced_matrix = [list(first_row)]
    for i in range(1, matrix.rows):
        # Perform reduction and leave the residual as first element of the new row.
        old_row = matrix.row(i)
        row_value = old_row[0]
        new_row = old_row - math.floor(row_value / min_value) * first_row

        reduced_matrix.append(list(new_row))

    return Matrix(reduced_matrix)


def col_reduce(matrix: Matrix) -> Matrix:
    return row_reduce(matrix.transpose()).transpose()
