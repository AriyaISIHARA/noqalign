# noqalign

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

## Requirement

python>=(2.7|3.5)

## Usage

```
noqalign [-a{+-}] [-p{+-}] [in-file] [out-file]
```

### Options

- a(lign)

  - `+(default)` aligns `# noqa: F401` comments to placed at the same column.
  - `-` does not align.
  
- p(ut)

  - `+(default)` puts `# noqa: F401` comments to every `import` lines.
  - `-` does not put any new comment.

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

Any PR, especially satisfying the above issues,
or testcases criticizing the issues, is very welcome.
(For testcases, please `@skip` new testcases
so that the PR can be directly merged)


## Author

[Ariya ISIHARA](https://github.com/AriyaISIHARA)
