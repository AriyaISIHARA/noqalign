# noqalign

To be under development.

## Overview

The present tool put and align block comments `# noqa: F401`
to every line that matches to
```
/^(from¥s+¥.?¥w+¥s+)?import¥s+¥.?¥w+(¥s+as¥s+¥w+)(¥s*¥()?(¥s+#¥s+noqa¥s*:¥s*F401)?¥s*$/

# [from <something>] import <something> [as <something>] [(] [# noqa: F401]
```
basically to be applied to `__init__.py` files.

## Usage

```
noqalign [-a{+-}] [-p{+-}] [in-file] [out-file]
```

### Options

- a(lign)

  - `+(default)` alignes `# noqa: F401` comments to placed at the same column.
  - `-` does not align.
  
- p(ut)

  - `+(default)` puts `# noqa: F401` comments to every `import` lines.
  - `-` does not put any new comment.

- <in-file> specifies input filename. `-`(default) reads STDIN.

- <out-file> specifies output filename.

  `-` writes to STDOUT.
  When omitted, overwrites to <in-file> itself if <in-file> is not STDIN;
  outputs to STDOUT otherwise.
