"""Noqalign"""

import argparse
from io import StringIO
import logging
import re
import sys

from .invoke_flake8 import invoke_flake8


logger = logging.getLogger('noqalign')
__version__ = '1.1.0'


if sys.version_info[0] < 3:
    import codecs

    def print_(o, file):
        if file is None:
            file = sys.stdout
        if isinstance(o, str):
            o = codecs.decode(o, 'utf8')
        file.write(o)
        file.write(u'\n')
else:
    def print_(o, file):
        if file is None:
            file = sys.stdout
        file.write(o)
        file.write('\n')


class Noqalign(object):
    """noqalign

    puts or aligns block comments '# noqa: F401'
    where presumed preferred.
    """

    def __init__(self, lines):
        self._lines = lines

    def write(self, put=None, align=None, file=None):
        """Apply noqalign

        Applies noqalign conversion to the given string
        and write the result to `file` (default: STDOUT).
        The option `put` puts new 'noqa F401' comments.
        The option `align` aligns all the 'noqa F401' comments.
        """
        if put is None:
            put = True
        if align is None:
            align = True

        col = self._calc_alignment(put, align)
        for line in self._lines:
            line.write(file, put, col)

    def _calc_alignment(self, put, align):
        if not align:
            return 0
        c = _LineWithImport if put else _LineWithImportWithNoqa

        result = 0
        for line in self._lines:
            if isinstance(line, c):
                col = line.std_noqa_col
                if result < col:
                    result = col
        return result

    def applied(self, put=None, align=None):
        """Wrapper of write() which returns string"""
        with StringIO() as sio:
            self.write(put=put, align=align, file=sio)
            return sio.getvalue()

    @classmethod
    def from_file(cls, file):
        """Setup noqalign from file (s.a. from_str)"""
        return cls([_Line.from_str(line.rstrip('\n')) for line in file])

    @classmethod
    def from_file_with_flake8(cls, file):
        lines = file.readlines()
        line_numbers = invoke_flake8(''.join(lines), logger.warning)
        return cls([
            _LineWithImportWithoutNoqa(line.rstrip('\n').rstrip())
            if line_numbers and (linenum in line_numbers)
            else _Line.from_str(line.rstrip('\n'), _LineWithoutImport)
            for linenum, line in enumerate(lines, 1)
        ])

    @classmethod
    def commandline(cls, args):
        parsed_args = cls._parsearg(args)

        put = parsed_args.put
        align = parsed_args.align
        flake8 = parsed_args.flake8
        infile = parsed_args.infile
        outfile = parsed_args.outfile

        if flake8:
            constructor = cls.from_file_with_flake8
        else:
            constructor = cls.from_file

        if outfile is None:
            outfile = infile
        if infile == '-':
            nql = constructor(sys.stdin)
        else:
            with open(infile) as fin:
                nql = constructor(fin)
        if outfile == '-':
            nql.write(put=put, align=align)
        else:
            with open(outfile, 'w') as fout:
                nql.write(put=put, align=align, file=fout)

    @classmethod
    def _parsearg(cls, args):
        prog = "noqalign %s" % __version__
        description = Noqalign.__doc__[10:]
        p = argparse.ArgumentParser(prog=prog, description=description)
        for opt in ('put', 'align'):
            help_pos = "%ss noqa block comments(default)" % opt
            help_neg = "does not %s noqa block comments" % opt
            p.add_argument(
                '-%s' % opt[0], '--%s' % opt,
                action='store_true',
                dest=opt,
                default=None,
                help=help_pos
            )
            p.add_argument(
                '-%s-' % opt[0], '--%s-' % opt,
                action='store_false',
                dest=opt,
                default=None,
                help=help_neg
            )
        p.add_argument(
            '-f', '--flake8',
            action='store_true',
            dest='flake8',
            default=None,
            help="invokes 'flake8' to detect lines to put noqa comment to"
        )
        p.add_argument(
            'infile',
            action='store', nargs='?', default='-',
            help="input filename; - for standard input(default)"
        )
        p.add_argument(
            'outfile',
            action='store', nargs='?', default=None,
            help=(
                "output filename; - for standard output"
                " (default is <infile>)"
            )
        )
        return p.parse_args(args)


class _Line(object):
    """Text line with importation and noqa information"""

    def write(self, file, put, column):
        raise NotImplementedError("abstract method")

    @property
    def std_noqa_col(self):
        raise NotImplementedError("abstract method")

    @classmethod
    def from_str(cls, text, without_noqa_cls=None):
        m = re.match(
            r'(?P<body>(?:from\s+\.?\w+\s+)?'
            r'import(?:\s+\.?\w+(?:\s+as\s+\w+)?|\s*\())'
            r'(?P<noqa>\s+#\s+noqa\s*:\s*F401)?\s*$',
            text,
            re.UNICODE
        )
        if not m:
            return _LineWithoutImport(text)
        body = m.group('body')
        noqa = m.group('noqa')
        if noqa:
            return _LineWithImportWithNoqa(body, noqa)
        return (without_noqa_cls or _LineWithImportWithoutNoqa)(body)


class _LineWithoutImport(_Line):
    def __init__(self, body):
        self._body = body

    def write(self, file, put, column):
        print_(self._body, file=file)

    @property
    def std_noqa_col(self):
        return 0


class _LineWithImport(_Line):
    def __init__(self, body):
        self._body = body

    @property
    def std_noqa_col(self):
        return len(self._body)

    def _std_noqa(self, column):
        return '%-*s  # noqa: F401' % (column, self._body)


class _LineWithImportWithoutNoqa(_LineWithImport):
    def __init__(self, body):
        super(_LineWithImportWithoutNoqa, self).__init__(body)

    def write(self, file, put, column):
        if put:
            o = self._std_noqa(column)
        else:
            o = self._body
        print_(o, file=file)


class _LineWithImportWithNoqa(_LineWithImport):
    def __init__(self, body, noqa):
        super(_LineWithImportWithNoqa, self).__init__(body)
        self._noqa = noqa

    def write(self, file, put, column):
        if column:
            o = self._std_noqa(column)
        else:
            o = self._body + self._noqa
        print_(o, file=file)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    Noqalign.commandline(args)


if __name__ == '__main__':
    main()
