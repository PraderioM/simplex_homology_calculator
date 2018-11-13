import os
import tkinter as tk
from tkinter import filedialog

from input_output import read_file, print_homology_groups
from mathematics import get_homology_groups


class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Instructions for using the GUI.
        self._instructions_input = tk.Label(self, text="Enter path to input file containing maximal faces", anchor="w")
        self._instructions_output = tk.Label(self, text="Enter path to file where results will be written", anchor="w")

        # Elements necessary for introducing input data.
        self._input_path = tk.StringVar()
        self._input_path_entry = tk.Entry(self, textvariable=self._input_path)  # path to json.
        self._input_path.set("")
        # button to browse for input.
        browse_input = tk.Button(self, text="···", command=lambda: self._browse(input_=True))

        # Elements necessary for returning output data.
        self._output_path = tk.StringVar()
        self._output_path_entry = tk.Entry(self, textvariable=self._output_path)  # path to output.
        self._output_path.set("")
        # button to browse for output.
        browse_output = tk.Button(self, text="···", command=lambda: self._browse(input_=False))

        # Button to compute homology.
        compute = tk.Button(self, text="compute homology", command=self._compute_homology)

        # Lay the widgets out on the screen.
        # Input
        self._instructions_input.grid(row=0, column=0, columnspan=5, pady=5, padx=5)
        self._input_path_entry.grid(row=1, column=0, columnspan=4, pady=5, padx=5)
        browse_input.grid(row=1, column=4, pady=5, padx=5)

        # Output.
        self._instructions_output.grid(row=2, column=0, columnspan=5, pady=5, padx=5)
        self._output_path_entry.grid(row=3, column=0, columnspan=4, pady=5, padx=5)
        browse_output.grid(row=3, column=4, pady=5, padx=5)

        # Result.
        compute.grid(row=4, column=0, pady=5, padx=5)

        # add event listener to add team member or generate teams when pressing enter key.
        self.master.bind('<Return>', self._compute_homology)

    def _browse(self, input_: bool):
        message = "Select {} file".format("input" if input_ else "output")
        path = filedialog.askopenfilename(initialdir=os.path.expanduser('~'),
                                          title=message)

        if input_:
            self._input_path.set(path)
        else:
            self._output_path.set(path)

    def _compute_homology(self):
        print('Hi')
        maximal_faces = read_file(file_path=self._input_path_entry.get())
        print(maximal_faces)
        homology_groups = get_homology_groups(faces=maximal_faces)
        print(homology_groups)
        print_homology_groups(homology_groups=homology_groups,
                              file_path=self._output_path_entry.get())
