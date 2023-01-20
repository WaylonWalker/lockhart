# Lockhart

[![PyPI - Version](https://img.shields.io/pypi/v/lockhart.svg)](https://pypi.org/project/lockhart)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lockhart.svg)](https://pypi.org/project/lockhart)

---

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```bash
pip install lockhart
## or with pipx
pipx install lockhart
```

You will need an openai key, you can obtain one from their
[website](https://beta.openai.com/account/api-keys). Once you have it then set
your `OPENAI_API_KEY` environment variable.

```bash
export OPENAI_API_KEY='sk-***'
```

Lockhart it currently very crude, it works out of the clipboard. Copy a
function to your clipboard, run `lockhart docstring` then paste the docstring
in.

## License

`lockhart` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
