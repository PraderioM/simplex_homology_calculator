from typing import List, Optional

from utils import Face, Group


def get_face_from_str(face_str: str) -> Face:
    face_str = face_str.replace('(', '').replace(')', '')
    face = face_str.split(',')

    return Face([int(value) for value in face])


def read_file(file_path: str) -> List[Face]:
    with open(file_path, 'r') as input_file:
        # Join all lines separating different lines with a semicolon.
        lines = input_file.readlines()
        faces_str = ';'.join(lines).strip()
        faces_str = faces_str.replace(' ', '').replace('),(', ');(')

        # Separate all input faces
        faces = faces_str.split(';')
        out_faces = [get_face_from_str(face) for face in faces]

    return out_faces


def print_homology_groups(homology_groups: List[Group],
                          file_path: Optional[str] = None):
    if file_path is None:
        output_file = None
    else:
        output_file = open(file_path, 'w')

    for i, homology_group in enumerate(homology_groups):
        line = 'H{}:\t{}'.format(i, homology_group)

        if output_file is None:
            print(line)
        else:
            line += '\n'
            output_file.write(line)

    line = 'Hi:\t0\tfor i greater or equal to {}'.format(len(homology_groups))
    if output_file is None:
        print(line)
    else:
        line += '\n'
        output_file.write(line)

    if output_file is not None:
        output_file.close()
