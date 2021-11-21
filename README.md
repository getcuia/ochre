[![PyPI](https://img.shields.io/pypi/v/ochre)](https://pypi.org/project/ochre/)
[![Python package](https://github.com/getcuia/ochre/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/ochre/actions/workflows/python-package.yml)
[![PyPI - License](https://img.shields.io/pypi/l/ochre)](https://github.com/getcuia/ochre/blob/main/LICENSE)

# [ochre](https://github.com/getcuia/ochre#readme) 🏜️

<div align="center">
    <img class="hero" src="https://github.com/getcuia/ochre/raw/main/banner.jpg" alt="ochre" width="33%" />
</div>

> A down-to-earth approach to colors

ochre is a tiny Python package for working with colors in a pragmatic way. The
focus is on simplicity and ease of use, but also on human perception.

## Features

-   🎨 Focus on [RGB](https://en.wikipedia.org/wiki/RGB_color_model) and
    [HCL](https://en.wikipedia.org/wiki/HCL_color_space) color spaces
-   🖥️ Web color names
-   ♻️ Color conversions that easily integrate with the
    [standard `colorsys` module](https://docs.python.org/3/library/colorsys.html)
-   🗑️ Zero dependencies
-   🐍 Python 3.8+

## Installation

```console
$ pip install ochre
```

## Usage

```python
In [1]: from ochre import Hex

In [2]: color = Hex("#CC7722")

In [3]: color.web_color
Out[3]: WebColor('peru')

In [4]: color = color.hcl

In [5]: color.hue
Out[5]: 0.6373041934059377

In [6]: import math

In [7]: color.hue += math.radians(30)

In [8]: color.hue
Out[8]: 1.1609029690042365

In [9]: color.web_color
Out[9]: WebColor('goldenrod')
```

## Credits

[Photo](https://github.com/getcuia/ochre/raw/main/banner.jpg) by
[Nicola Carter](https://unsplash.com/@ncarterwilts?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on
[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).
