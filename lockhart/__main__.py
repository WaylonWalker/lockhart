# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == '__main__':
    from .cli import docgen

    sys.exit(docgen())
