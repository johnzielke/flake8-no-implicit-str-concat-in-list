[![PyPI version](https://badge.fury.io/py/flake8-no-implicit-str-concat-in-list.svg)](https://badge.fury.io/py/flake8-no-implicit-str-concat-in-list)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-no-implicit-str-concat-in-list)
[![Downloads](https://pepy.tech/badge/flake8-no-implicit-str-concat-in-list/month)](https://pepy.tech/project/flake8-no-implicit-str-concat-in-list)
[![Github Actions](https://github.com/johnzielke/flake8-no-implicit-str-concat-in-list/workflows/build/badge.svg?event=push)](https://github.com/johnzielke/flake8-no-implicit-str-concat-in-list/actions)
[![Codecov](https://codecov.io/gh/johnzielke/flake8-no-implicit-str-concat-in-list/branch/master/graph/badge.svg)](https://codecov.io/gh/johnzielke/flake8-no-implicit-str-concat-in-list)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)



flake8-no-implicit-str-concat-in-list
=========================

[Flake8][] plugin that forbids implicit str/bytes literal concatenations inside literals such as lists, sets and tuples.

    # NG
    a = ["aaa",
         "bbb"
         "ccc"]

    # OK
    print('foobar' 'baz')
    a = ["aaa",
         "bbb"
         + "ccc"]
    b = b'abcdef'
    s = ('abc'
        'def')
 

Installation
------------

Install via pip:

    pip install flake8-no-implicit-str-concat-in-list


Violation Codes
---------------

The plugin uses the prefix `ICL`, short for no **i**mplicit string **c**oncatenation in **l**ists.
Unfortunately flake8 only allows three characters for the error code prefix.

| Code  | Description                                                |
| ----- | ---------------------------------------------------------- |
| ICL122 | Implicitly concatenated bytes literals in list literal over multiple lines.      |
| ICL112 | Implicitly concatenated bytes literals in list literal.                          |
| ICL121 | Implicitly concatenated str literals in list literal over multiple lines.        |
| ICL111 | Implicitly concatenated str literals in list literal.                            |
| ICL222 | Implicitly concatenated bytes literals in tuple literal over multiple lines.     |
| ICL212 | Implicitly concatenated bytes literals in tuple literal.                         |
| ICL221 | Implicitly concatenated str literals in tuple literal over multiple lines.       |
| ICL211 | Implicitly concatenated str literals in tuple literal.                           |
| ICL322 | Implicitly concatenated bytes literals in set literal over multiple lines.       |
| ICL312 | Implicitly concatenated bytes literals in set literal.                           |
| ICL321 | Implicitly concatenated str literals in set literal over multiple lines.         |
| ICL311 | Implicitly concatenated str literals in set literal.                             |


Other Plugins & Linters
-----------------------

- [**flake8-implicit-str-concat**][flake8-implicit-str-concat]
  Flake8 plugin to encourage correct string literal concatenation.
  This plugin is different from `flake8-no-implicit-str-concat-in-list`
  because this plugin prefers implicit concatenations over explicit `+`
  operators when concatenating literals even inside lists, tuples and set literals.
- [**wemake-python-styleguide**][wemake-python-styleguide]
  Set of strict flake8 rules with several plugins as dependencies.
  It implements `WPS326 Found implicit string concatenation`, which also
  checks implicit string concatenations, as one of the many rules it defines.
- [**pylint**][pylint] 
  This linter has `implicit-str-concat` rule.
  By default it only looks for occurrences of implicit concatenations on the
  same line, but it has `--check-str-concat-over-line-jumps=y` option
  to enable checking of concatenations over multiple lines.
- [**flake8-no-implicit-concat**][flake8-no-implicit-concat] 
  This linter has `no_implicit_concat` rule.
  It also looks for implicit string concatenation but in all contexts,
  not just in lists.

Development
-----------

Use tools like Pipenv:

    pipenv run python -m pip install -e .[dev]
    pipenv run make check


License
-------

This software is released under MIT license. See `LICENSE` for details.

The code was derived from [flake8-no-implicit-concat][], which is developed by
10sr and also released under MIT license.



[Flake8]: https://flake8.pycqa.org/en/latest/
[flake8-implicit-str-concat]: https://github.com/keisheiled/flake8-implicit-str-concat
[flake8-no-implicit-concat]: https://github.com/10sr/flake8-no-implicit-concat
[wemake-python-styleguide]: https://github.com/wemake-services/wemake-python-styleguide
[pylint]: https://github.com/PyCQA/pylint
