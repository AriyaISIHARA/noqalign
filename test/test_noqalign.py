import os
from unittest import TestCase


class NoqalignTest(TestCase):
    def _test_noqalign_core(self, sample_name):
        from noqalign import Noqalign

        self.maxDiff = None

        in_file = '%s.src' % sample_name
        in_src = _read_file(in_file)
        p_src = _read_file('%s_p.src' % sample_name)
        a_src = _read_file('%s_a.src' % sample_name)
        pa_src = _read_file('%s_pa.src' % sample_name)

        with open(_testpath(in_file), 'r') as fin:
            nql = Noqalign.from_file(fin)
        self.assertEqual(nql.applied(), pa_src)
        self.assertEqual(nql.applied(put=True), pa_src)
        self.assertEqual(nql.applied(put=False), a_src)
        self.assertEqual(nql.applied(align=True), pa_src)
        self.assertEqual(nql.applied(align=False), p_src)
        self.assertEqual(nql.applied(put=True, align=True), pa_src)
        self.assertEqual(nql.applied(put=True, align=False), p_src)
        self.assertEqual(nql.applied(put=False, align=True), a_src)
        self.assertEqual(nql.applied(put=False, align=False), in_src)

    def test_noqalign_core_original(self):
        self._test_noqalign_core('sample')

    def test_noqalign_core_fix_issue4(self):
        self._test_noqalign_core('fix_issue4')

    def _test_cmd_stdin_stdout(self, args, output_type, srcname='sample'):
        from io import StringIO
        import sys
        from noqalign import Noqalign

        stdin_org = sys.stdin
        stdout_org = sys.stdout

        def cleanup():
            sys.stdin.close()
            sys.stdout.close()
            sys.stdin = stdin_org
            sys.stdout = stdout_org

        self.addCleanup(cleanup)
        sys.stdin = open(_testpath('%s.src' % srcname))
        sys.stdout = StringIO()
        expected = _read_file('%s%s.src' % (srcname, output_type))

        Noqalign.commandline(args)
        self.assertEqual(sys.stdout.getvalue(), expected)

    def test_noqalign_cmd_stdin_stdout_pNaN(self):
        self._test_cmd_stdin_stdout([], '_pa')

    def test_noqalign_cmd_stdin_stdout_pNaF(self):
        self._test_cmd_stdin_stdout(['-a-'], '_p')

    def test_noqalign_cmd_stdin_stdout_pFaN(self):
        self._test_cmd_stdin_stdout(['-p-'], '_a')

    def test_noqalign_cmd_stdin_stdout_pFaF(self):
        self._test_cmd_stdin_stdout(['-a-', '-p-'], '')

    def test_impl_issue6_pa(self):
        self._test_cmd_stdin_stdout([], '_pa', 'impl_issue6')

    def test_impl_issue6_paf(self):
        self._test_cmd_stdin_stdout(['-f'], '_paf', 'impl_issue6')

    def _test_cmd_stdin_fileout(self, args, output_type, outfile):
        import sys
        from noqalign import Noqalign

        stdin_org = sys.stdin

        def cleanup():
            sys.stdin.close()
            sys.stdin = stdin_org
            os.remove(_testpath(outfile))

        self.addCleanup(cleanup)
        sys.stdin = open(_testpath('sample.src'))
        expected = _read_file('sample%s.src' % output_type)

        Noqalign.commandline(args)
        output = _read_file(outfile)
        self.assertEqual(output, expected)

    def test_noqalign_cmd_stdin_fileout_pNaN(self):
        outfile = 'fileout_test_tmp.src'
        self._test_cmd_stdin_fileout(
            ['-', _testpath(outfile)], '_pa', outfile
        )

    def test_noqalign_cmd_stdin_fileout_pNaF(self):
        outfile = 'fileout_test_tmp.src'
        self._test_cmd_stdin_fileout(
            ['-a-', '-', _testpath(outfile)], '_p', outfile
        )

    def test_noqalign_cmd_stdin_fileout_pFaN(self):
        outfile = 'fileout_test_tmp.src'
        self._test_cmd_stdin_fileout(
            ['-p-', '-', _testpath(outfile)], '_a', outfile
        )

    def test_noqalign_cmd_stdin_fileout_pFaF(self):
        outfile = 'fileout_test_tmp.src'
        self._test_cmd_stdin_fileout(
            ['-a-', '-p-', '-', _testpath(outfile)], '', outfile
        )

    def _test_cmd_filein_stdout(self, args, output_type):
        from io import StringIO
        import sys
        from noqalign import Noqalign

        stdout_org = sys.stdout

        def cleanup():
            sys.stdout.close()
            sys.stdout = stdout_org

        self.addCleanup(cleanup)
        sys.stdout = StringIO()
        expected = _read_file('sample%s.src' % output_type)

        Noqalign.commandline(args)
        self.assertEqual(sys.stdout.getvalue(), expected)

    def test_noqalign_cmd_filein_stdout_pNaN(self):
        infile = _testpath('sample.src')
        self._test_cmd_filein_stdout([infile, '-'], '_pa')

    def test_noqalign_cmd_filein_stdout_pNaF(self):
        infile = _testpath('sample.src')
        self._test_cmd_filein_stdout(['-a-', infile, '-'], '_p')

    def test_noqalign_cmd_filein_stdout_pFaN(self):
        infile = _testpath('sample.src')
        self._test_cmd_filein_stdout(['-p-', infile, '-'], '_a')

    def test_noqalign_cmd_filein_stdout_pFaF(self):
        infile = _testpath('sample.src')
        self._test_cmd_filein_stdout(['-a-', '-p-', infile, '-'], '')

    def _test_cmd_file_overwrite(self, args, output_type, tmpfile):
        import shutil
        from noqalign import Noqalign

        def cleanup():
            os.remove(_testpath(tmpfile))

        self.addCleanup(cleanup)
        expected = _read_file('sample%s.src' % output_type)
        shutil.copy(_testpath('sample.src'), _testpath(tmpfile))

        Noqalign.commandline(args)
        result = _read_file(tmpfile)
        self.assertEqual(result, expected)

    def test_noqalign_cmd_file_overwrite_pNaN(self):
        tmpfile = 'test_noqalign_cmd_file_overwrite_sample_src.py'
        self._test_cmd_file_overwrite(
            [_testpath(tmpfile)], '_pa', tmpfile
        )

    def test_noqalign_cmd_file_overwrite_pNaF(self):
        tmpfile = 'test_noqalign_cmd_file_overwrite_sample_src.py'
        self._test_cmd_file_overwrite(
            ['-a-', _testpath(tmpfile)], '_p', tmpfile
        )

    def test_noqalign_cmd_file_overwrite_pFaN(self):
        tmpfile = 'test_noqalign_cmd_file_overwrite_sample_src.py'
        self._test_cmd_file_overwrite(
            ['-p-', _testpath(tmpfile)], '_a', tmpfile
        )

    def test_noqalign_cmd_file_overwrite_pFaF(self):
        tmpfile = 'test_noqalign_cmd_file_overwrite_sample_src.py'
        self._test_cmd_file_overwrite(
            ['-a-', '-p-', _testpath(tmpfile)], '', tmpfile
        )


def _testpath(path):
    rootdir = os.path.dirname(__file__)
    return os.path.join(rootdir, path)


def _read_file(fname):
    fpath = _testpath(fname)
    with open(fpath) as fin:
        return fin.read()
