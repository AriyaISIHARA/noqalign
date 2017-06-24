def invoke_flake8(buf_lines):
    """Invokes flake8.

    pipe `buf_lines` into 'flake8 - --exit-zero'
    and parse output to find 'stdin:%(line)d:%(col)d F401...'
    to return tuple of line numbers where flake8 alerted F401.
    """

    # tentative
    return 1, 2, 5
