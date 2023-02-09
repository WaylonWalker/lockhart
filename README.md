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

## lockhart tui

```bash
lockhart tui
```

https://user-images.githubusercontent.com/22648375/217840817-04626da4-8558-4fc4-8b05-ff0e57a2a28b.mp4

### keys

* C - Create new code
* e - edit return value from history item
* E - open an empty edit template
* o - open the current prompt from history
* j - next item from history
* k - prev item from history
* q - quit
* d - toggle dark mode
* b - toggle sidebar of preset prompts
* G - open an empty prompt for writing a git commit

### Editing prompts

Currently the tui runs the users configured `$EDITOR` in a subprocess, waits for the editor to close, and if the file was changed then it runs the prompt.  If the file was not changed then it does not run the prompt.

```bash
## mac/linux
export EDITOR=vim
 
## windows
set EDITOR=notepad
```

### closing vim

**:x** without a change to the content will not trigger a file change and the prompt will not run.  If you want to use the prompt as-is without edit close vim with **:wq**.

## CLI

### lockhart prompt run

You can also run stored prompts from the command line without the tui.

``` bash
## pipe text into your prompt
echo 'write a python3.10 hello world function' | lockhart prompt run code-create

## use the --text flag
lockhart prompt run code-create --text 'write a python3.10 hello world function' 

## directly edit your prompt with the editor
lockhart prompt run code-create --edit
```

The cli also handles text being piped into a prompt run.  You can still `--edit` it, or pipe the results somewhere.  Many of the commit messages in this repo were created using this.

``` bash
## pre-populate your commit message
git diff --staged | lockhart prompt run commit | git commit -evF -

## write a changelog entry for your current pr
gh pr diff | lockhart prompt run changelog --edit

## write a changelog entry for your current staged changes
git diff --staged | lockhart prompt run changelog --edit
```

### listing prompts

The cli can list all of the prompts configured in `~/.config/lockhart/lockhart.toml` using the cli.

``` bash
lockhart prompt list
```

## lockhart history

The cli can output your entire history as json.

``` bash
lockhart history list
```


--- 

## Original features that need re-implemented

These shouldn't be too bad to get re-implemented, but I think we need a pre-processor to be able to get this working.

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
