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

TBA
