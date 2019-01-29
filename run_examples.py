import os
from time import time
from glob import glob

from input_output import read_file, print_homology_groups
from mathematics import get_homology_groups

if __name__ == "__main__":
    examples_path = "./examples"
    examples = sorted(glob(os.path.join(examples_path, 'inputs/*')))
    for input_path in examples:
        file_name = os.path.basename(input_path)
        print("Time table for computing homology of simplex in {} (milliseconds).".format(file_name))
        reading_start = time()
        maximal_faces = read_file(file_path=input_path)
        computation_start = time()
        reading_time = (computation_start - reading_start)*1000
        homology_groups = get_homology_groups(faces=maximal_faces)
        write_start = time()
        computation_time = (write_start - computation_start)*1000

        output_path = os.path.join(examples_path, "outputs", file_name)
        computation_end = time()
        writing_time = (computation_end - write_start)*1000

        total_time = (computation_end - reading_start)*1000
        print("reading_time:\t\t{}\t({:.1f}%)".format(reading_time, 100*reading_time/total_time))
        print("computation_time:\t{}\t({:.1f}%)".format(computation_time, 100*computation_time/total_time))
        print("writing_time:\t\t{}\t({:.1f}%)".format(writing_time, 100*writing_time/total_time))
        print("total_time:\t\t\t{}".format(total_time))
        print("\n")

        print_homology_groups(homology_groups=homology_groups,
                              file_path=output_path)
