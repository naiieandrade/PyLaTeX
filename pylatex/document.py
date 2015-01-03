# -*- coding: utf-8 -*-
"""
    pylatex.document
    ~~~~~~~

    This module implements the class that deals with the full document.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import subprocess
from .package import Package
from .command import Command
from .utils import dumps_list
from .base_classes import BaseLaTeXContainer


class Document(BaseLaTeXContainer):

    """
    A class that contains a full latex document. If needed, you can append
    stuff to the preamble or the packages if needed.
    """

    def __init__(self, filename='default_filename', documentclass='article',
                 fontenc='T1', inputenc='utf8', author=None, title=None,
                 date=None, data=None):
        self.filename = filename

        if isinstance(documentclass, Command):
            self.documentclass = documentclass
        else:
            self.documentclass = Command('documentclass', documentclass)

        fontenc = Package('fontenc', option=fontenc)
        inputenc = Package('inputenc', option=inputenc)
        packages = [fontenc, inputenc, Package('lmodern')]

        self.preamble = []

        if title is not None:
            self.preamble.append(Command('title', title))
        if author is not None:
            self.preamble.append(Command('author', author))
        if date is not None:
            self.preamble.append(Command('date', date))

        super().__init__(data, packages=packages)

    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        document = r'\begin{document}'

        document += dumps_list(self)

        document += r'\end{document}'

        # Needed to propagate the packages
        super().dumps()

        head = self.documentclass.dumps()

        head += self.dumps_packages()
        head += dumps_list(self.preamble)

        return head + document

    def generate_tex(self):
        """Generates a .tex file."""
        newf = open(self.filename + '.tex', 'w')
        self.dump(newf)
        newf.close()

    def generate_pdf(self, clean=True):
        """Generates a pdf"""
        self.generate_tex()

        command = 'pdflatex --jobname="' + self.filename + '" "' + \
            self.filename + '.tex"'

        subprocess.check_call(command, shell=True)

        if clean:
            subprocess.call('rm "' + self.filename + '.aux" "' +
                            self.filename + '.log" "' +
                            self.filename + '.tex"', shell=True)
