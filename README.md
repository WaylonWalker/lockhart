<img src="https://user-images.githubusercontent.com/22648375/213756335-5695774d-fdf6-4afd-920f-36da7e2decf3.png" alt="Markata" width="250" align=right>

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

## Instructions

You will need an openai key, you can obtain one from their
[website](https://beta.openai.com/account/api-keys). Once you have it then set
your `OPENAI_API_KEY` environment variable.

```bash
export OPENAI_API_KEY='sk-***'
```

Lockhart it currently very crude, it works out of the clipboard. Copy a
function to your clipboard, run `lockhart docstring` then paste the docstring
in.

```bash
# copy a function
lockhart docstring
# paste in your docstring
```

> yes it just uses the clipboard for now. - the `develop` branch includes new configuration and commands.

## Docstring Examples

```python
def add(a, b):
    """

    Add two numbers together.

    Args:
        a (int): The first number to add.
        b (int): The second number to add.

    Returns:
        int: The sum of the two numbers.

    Example:
        add(2, 3) -> 5

    """
    return a + b
```

Without even type hinting the arguments `lockhart` can see that this function is using pandas.

```python
def get_summary_data(df):
    """
    This function takes a dataframe as an argument and returns a summary of the data grouped by column A.

    Args:
        df (DataFrame): The dataframe to be summarized.

    Returns:
        DataFrame: A summary of the data grouped by column A, containing the sum of columns C and D.

    Example:
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9], 'D': [10, 11, 12]})
        get_summary_data(df)
    """
    df.groupby("A")[["C", "D"]].sum()
```

Here is an example from the fastapi docs. It writes a correct docstring to
describe the function, but misses out that its a fastapi route without more
context than just the function.

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    Update an item in the database.

    This function takes an item_id and an item object as parameters and updates the item in the database.

    Args:
        item_id (int): The id of the item to be updated.
        item (Item): The item object to be updated.

    Returns:
        dict: A dictionary containing the item_id and the updated item.

    Example:
        results = update_item(1, {'name': 'Foo', 'price': 10.99})
    """
    results = {"item_id": item_id, "item": item}
    return results
```

## Examples Refactor

```python
def add(a, b):
    return a + b

# refactor the following code to compute the ratio of the two numbers

def ratio(a, b):
    return a / b
```

```python
# Before
def get_summary_data(df):
    df.groupby("A")[["C", "D"]].sum()

# refactor the following code to also return the averages

# After
def get_summary_data(df):
    df.groupby("A")[["C", "D"]].agg(["sum", "mean"])
```

Run `lockhart refactor`, then set the prompt to `refactor the following code to
accept a parameter item_name`. It did a great job at adding it to the
arguments list, type hinting it to a string, but again missed that this is a
fastapi route and we wanted to also update the decorator.

````python

``` python
# before
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# refactor the following code to accept a parameter item_name

# after
@app.put("/items/{item_id}")
def update_item(item_id: int, item_name: str, item: Item):
    results = {"item_id": item_id, "item_name": item_name, "item": item}
    return results
````

## License

`lockhart` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
