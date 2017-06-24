import re
from subprocess import CalledProcessError, Popen, PIPE


def invoke_flake8(buf_str, warning):
    """Invokes flake8.

    pipe `buf_lines` into 'flake8 - --exit-zero'
    and parse output to find 'stdin:%(line)d:%(col)d F401...'
    to return tuple of line numbers where flake8 alerted F401.
    """

    try:
        flake8_input = buf_str.encode('utf-8')
    except UnicodeEncodeError as e:
        warning("encoding flake8 input failed: %s", e)
        return None

    try:
        p = Popen(
            ['flake8', '-', '--exit-zero'],
            stdin=PIPE, stdout=PIPE
        )
        flake8_output_b, _ = p.communicate(flake8_input)
    except (OSError, CalledProcessError) as e:
        warning("invoking flake8 failed: %s", e)
        return None

    try:
        flake8_output = flake8_output_b.decode('utf-8', 'ignore')
    except UnicodeDecodeError as e:
        warning("decoding flake8 output failed: %s", e)
        return None

    return _find_lines(flake8_output, 'stdin', 'F401')


def _find_lines(flake8_output, fname, code):
    lines = set()
    pattern = (
        r'^%s:(?P<linenum>[0-9]+):[0-9]+:\s*%s'
        % (re.escape(fname), re.escape(code))
    )
    for m in re.finditer(
            pattern,
            flake8_output,
            re.MULTILINE | re.UNICODE
    ):
        linenum = int(m.group('linenum'))
        lines.add(linenum)
    return lines
