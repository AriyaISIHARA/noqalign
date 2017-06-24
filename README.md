# noqalign

To be under development.

## Overview

The present tool put and align block comments `# noqa: F401`
to every line that matches to
```
/^(from¥s+¥.?¥w+¥s+)?import¥s+¥.?¥w+(¥s+as¥s+¥w+)?(¥s*¥()?(¥s+#¥s+noqa¥s*:¥s*F401)?¥s*$/

# [from <something>] import <something> [as <something>] [(] [# noqa: F401]
```
basically to be applied to `__init__.py` files.

## History
- 1.0.0  First release
- 1.0.1  The bug reported in Issue #4 fixed
- 1.1.0  Implemented the option `--flake8` (Issue #6)

## Requirement

- python>=(2.7|3.5)
- flake8 (only when invoked with `--flake8` option)

    Noqalign, invoked with `--flake8` option, internally invokes flake8
    with `flake8 - --exit-zero` from shell.
    Thus, flake8 of a version corresponding to installed (or activated)
    python should be installed, or any equivalent should be
    installed and aliased to `flake8`, so that
    `flake8 - --exit-zero` from shell will work anyway.

## Usage

```
noqalign [-a{+-}] [-p{+-}] [-f] [in-file] [out-file]
```

### Options

- a(lign)

  - `+(default)` aligns `# noqa: F401` comments to placed at the same column.
  - `-` does not align.
  
- p(ut)

  - `+(default)` puts `# noqa: F401` comments to every `import` lines.
  - `-` does not put any new comment.
  
- f(lake8)

  Internally invokes flake8 to decide which line to put `# noqa: F401` comment to.
  
  The option has no effect when `put` is inactivated.
  
  If `flake8 - --exit-zero` cannot be invoked from shell,
  noqalign does not put any new noqa comment; behaves as `put` is inactivated.

- <in-file> specifies input filename. `-`(default) reads STDIN.

- <out-file> specifies output filename.

  `-` writes to STDOUT.
  When omitted, overwrites to <in-file> itself if <in-file> is not STDIN;
  outputs to STDOUT otherwise.

## Install

Type and pray to press enter:

```
% git clone https://github.com/AriyaISIHARA/noqalign
% cd noqalign
% python setup.py install
```

## Contribution

Presently the author does not strongly intended
to upgrade the present tool any more.
The tools leaves many features to be improved:

- Processing all `__init__.py` files in a directory tree
- Support other kinds of block comments, maybe with regex
- Support backslash stuffs
- Support eol other than CR
- Implement `remove` option, which removes `# noqa: F401` comments;
    the all, or those which are unnecessary to keep flake8 silent.

Any PR, especially satisfying the above issues,
or testcases criticizing the issues, is very welcome.
(For testcases, please `@skip` new testcases
so that the PR can be directly merged)


## Author

[Ariya ISIHARA](https://github.com/AriyaISIHARA)
