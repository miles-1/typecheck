# Typecheck

## Description

This module provides a function, `checkType`, that allows for type enforcement of parameters, and auto-generates a message if this type is not fulfilled.

## Installation

Using `pip`:
```
pip install git+https://github.com/miles-1/typecheck.git
```

## Example

```python
def func(integer, str_from_options, tuple_of_ints, complex_dict1, complex_dict2):
    checkType(
        ("integer",             int,                    integer),
        ("str_from_options",    Ex("N","S","E","W"),    str_from_options),
        ("tuple_of_ints",       (int,),                 tuple_of_ints),
        ("complex_dict1",       {int: Op(str, float)},  complex_dict1),
        ("complex_dict2",       {(str,): Any()},        complex_dict2),
    )
    ...<function contents>...
```
*Note: `Ex` and `Op` are objects that are very similar to `tuple`s.* In the above code snippet, `checkType` will raise a `TypeError` if the parameter in each 3-tuple does not follow the given structure. The following table shows how each row would be handled by `checkType`:


|parameter name|structure|structure description|ex(s) correct|ex(s) incorrect|error if incorrect|
|-|-|-|-|-|-|
|`integer`|`int`|integer|`1`|`1.0`|`integer` must follow this structure:<br/>`{'Type': 'int'}`|
|`str_from_options`|`Ex("N","S","E","W")`|One of these `Ex`act values: `"N"`,`"S"`,`"E"`, or `"W"`|`"W"`|`"K"`, `"foo"`, 5|`str_from_options` must follow this structure:<br/>`{'Exact_Value': ['N', 'S', 'E', 'W']}`|
|`tuple_of_ints`|`[int,]`|List of integers|`[1,2,3]`, `[5]`|`1`, `[]`, `[1.0,2.0,3.0]`,<br/>`[5,6,7.0]`,<br/>`(1,2,3)`|`tuple_of_ints` must follow this structure:<br/>`{'Collection': 'tuple', 'Element_Structure': {'Type': 'int'}}`|
|`complex_dict1`|`{int: Op(str, float)}`|Dictionary where keys are integers and values have the `Op`tion of being strings or floats|`{1:1.0}`,<br/>`{4:0.9, 5:"foo", 6:1.1}`|`None`, `{}`, <br/>`{"hi":1.0}`,<br/>`{4:0.9, 5:"foo", 6:1.1}`|`complex_dict1` must follow this structure:<br/>`{'Collection': 'dict', 'Key_Structure': {'Type': 'int'}, 'Value_structure': {'Type': [1, 2, 3]}}`|
|`complex_dict2`|`{(str,): Any()}`|Dictionary where keys are tuples of strings and values can be `Any`thing|`{("q","k"): None}`,<br/>`{("i",): [1.23, "j"], ("yes","no"):1}`|`"k"`, `{}`,<br/>`{"bar":"foo", 6:1.1}`|`complex_dict2` must follow this structure:<br/>`{'Collection': 'dict', 'Key_Structure': {'Collection': 'tuple', 'Element_Structure': {'Type': 'str'}}, 'Value_structure': {'Type': 'Any'}}`|

## Usage

`checkType` accepts any number of 3-tuples of the following structure: `("argName", <expected>, <actual>)`

The following are the valid ways to create a value for `<expected>`. The symbols `<expd>`, `<expd1>`, etc below represent any valid value of `<expected>`.

### Terminal options:
1. `Any()`: Object of any type
2. `<Type>`: Object of type `<Type>`
3. `Op(<Type1>, <Type2>)`: Object of type `<Type1>` or `<Type2>` (`Op` is short for `Options`.)
4. `Ex("literal1", "literal2")`: Object from a set of allowed values (`Ex` is short for Exact Values. Assessed with `in`, so `2` would satisfy `Ex(2.0, 1.0)`.)
5. `Callable()`: Obj returns true with python's `callable` function
6. `Num(<args>, num_type=<Type>)`: Obj returns true if it is of type `num_type` and if it lays within specified bounds in `<args>`.

### Nesting options:
1. `Op(<expd1>, <expd2>)`: Object that has `<expd1>` or `<expd2>` structure
2. `(<expd1>, <expd2>)`: Tuple (*or other positional iterable*) where the first element has `<expd1>` structure, second has `<expd2>` structure
3. `(<expd>,)`: Tuple (*or other nondictlike iterable*) of elements that have `<expd>` structure
4. `(<expd>, <length>)`: Tuple (*or other measurable iterable*) of elements that have `<expd>` structure and integer length `<length>`
5. `{<expdkey>: <expdval>}`: Dictionary (*or other dictlike iterable*) where keys have `<expdkey>` structure and values have `<expdval>` structure