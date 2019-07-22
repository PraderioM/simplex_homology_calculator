from typing import List, Optional

from utils import Face, Group


def get_face_from_str(face_str: str) -> Face:
    face_str = face_str.replace('(', '').replace(')', '')
    face = face_str.split(',')

    return Face([int(value) for value in face])


def read_raw_data(raw_data: str) -> List[Face]:
    raw_data = raw_data.strip().replace('\n', '').replace(' ', '')
    while ';;' in raw_data:
        raw_data = raw_data.replace(';;', ';')
    raw_data = raw_data.replace('),(', ');(').replace(')(', ');(').strip()
    if raw_data[-1] == ';':
        raw_data = raw_data[:-1]

    # Separate all input faces
    faces = raw_data.split(';')
    out_faces = [get_face_from_str(face) for face in faces]

    return out_faces


def read_file(file_path: str) -> List[Face]:
    with open(file_path, 'r') as input_file:
        # Join all lines separating different lines with a semicolon.
        lines = input_file.readlines()
        raw_data = ';'.join(lines)
        out_faces = read_raw_data(raw_data)

    return out_faces


def get_homology_groups_formatted_text(homology_groups: List[Group]) -> str:
    text = ''
    for i, homology_group in enumerate(homology_groups):
        text += 'H{}:\t{}\n'.format(i, homology_group)

    text += 'Hi:\t0\tfor i greater or equal to {}'.format(len(homology_groups))

    return text


def print_homology_groups(homology_groups: List[Group],
                          file_path: Optional[str] = None):

    text = get_homology_groups_formatted_text(homology_groups=homology_groups)

    if file_path is None:
        print(text)
    else:
        with open(file_path, 'w') as output_file:
            output_file.write(text)
