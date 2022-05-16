# Code Style
LotBot implements a code style that is consistent with the [PEP8](https://www.python.org/dev/peps/pep-0008/), alongside
some other useful coding standards. Let's run through the code style guidelines for LotBot.

## Black Formatting
LotBot makes use of [black](https://black.readthedocs.io/en/stable/) code formatting. It's required for you to be in
compliance with black formatting. To do so, after you develop code it's recommended that you run `black python path/to/file.py` to 
format your code. Failure to do so will result in you being asked to re-format your code.

## Double Quotes
LotBot makes use of double quotes for all string literals. This is required for you to be in compliance with the code style. 
Black will automatically convert single quotes to double quotes.

## Simple not Complex
LotBot makes use of a simple not complex coding style. Simple is always better than complex,
there is no need to make your code overly complex and diffucult to read and understand.