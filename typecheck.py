import numpy as np
from dataclasses import dataclass

@dataclass
class _Type:
    _type: type
    positional: bool = True
    measurable: bool = True
    dictlike: bool = False

class _Iters:
    def __init__(self, *iter_lst):
        self.all = tuple(i._type for i in iter_lst)
        self.positional = tuple(i._type for i in iter_lst if i.positional)
        self.measurable = tuple(i._type for i in iter_lst if i.measurable)
        self.dictlike = tuple(i._type for i in iter_lst if i.dictlike)
        self.nondictlike = tuple(i._type for i in iter_lst if not i.dictlike)

allowed_iters = _Iters(
    _Type(tuple), 
    _Type(list), 
    _Type(dict, dictlike=True, measurable=False, positional=False), 
    _Type(set, positional=False),
    _Type(np.ndarray),
)

class Op(tuple):
    def __new__(cls, *args):
        args_lst = []
        for i in args:
            if isinstance(i, Op):
                for j in i:
                    if j not in args_lst:
                        args_lst.append(j)
            elif i not in args_lst:
                args_lst.append(i)
        if len(args_lst) == 1:
            return args_lst[0]
        elif any(isinstance(i, Any) for i in args_lst):
            return Any()
        elif len(args_lst) > 1:
            return super().__new__(cls, args_lst)
    
    def allType(self):
        return all(isinstance(i, type) for i in self)

class Ex(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)

class Any:
    pass

class Callable:
    pass

class Array:
    def __init__(self, *args):
        if args and any(not isinstance(arg, int) for arg in args):
            raise TypeError("All inputs for arrays must be integers")
        elif not args:
            self.shape = None
        else:
            self.shape = args
    
    def isMatch(self, array):
        if not isinstance(array, np.ndarray):
            return False
        elif self.shape:
            return array.shape == self.shape
        else:
            return True

class Num:
    def __init__(self, *info, num_type=None):
        # validate params
        checkType(
            ("num_type", Op(Ex(None), type), num_type)
        )
        # setup parameters
        if not len(info):
            info = (None, None)
        elif isinstance(info[0], tuple) and len(info) == 1:
            info = info[0]
        # set ranges
        if len(info) == 2 and all(map(self._isBoundType, info)):
            self.ranges = (info,)
        elif all(map(lambda x: isinstance(x, tuple), info)):
            self.ranges = info
        else:
            raise TypeError(f"info must be two bounds or a list of tuples of two bounds")
        # set types
        self.num_type = (int, float) if not num_type else \
            (num_type,) if isinstance(num_type, type) else num_type
    
    def isMatch(self, num):
        if not isinstance(num, self.num_type):
            return False
        for low, high in self.ranges:
            if None not in (low, high):
                if low <= num <= high:
                    return True
            elif low == None and high == None:
                return True
            elif low == None:
                if num <= high:
                    return True
            else:
                if low <= num:
                    return True
        return False
                
    def _isBoundType(self, num):
        return num == None or isinstance(num, (int, float))

class TL(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)

class _Dummy:
    def __new__(cls, obj):
        length = obj if isinstance(obj, int) else len(obj)
        if isinstance(obj, allowed_iters.dictlike):
            return {i: None for i in range(length)}
        else:
            return (None,) * length

def _stringify(iterable, iter_type):
    if isinstance(iterable, iter_type):
        if iter_type == Op:
            return list(e.__name__ for e in iterable)
        elif iter_type == Ex:
            return list(iterable)
    else:
        return iterable.__name__ if isinstance(iterable, type) else str(iterable)

def _getExpd(iterable):
    # structure of info is (expd_iter, expd_elem_type, length)
    info = [type(iterable)] + [None,] * 2
    for i in iterable:
        info[int(isinstance(i, int)) + 1] = i
    return info

def checkType(*info_tuple, print_errors=False):
    """
    info_tuple structure:
    ("argName", <expected>, <actual>)

    The following are the valid ways to create a value for <expected>. The symbols <expd>, <expd1>, etc below represent any valid value of <expected>.

    Terminal options:
    (1) Any()                         # obj of any type
    (2) <Type>                        # obj of type <Type>
    (3) Op(<Type1>, <Type2>)          # obj of type <Type1> or <Type2> (Op short for Options)
    (4) Ex("literal1", "literal2")    # obj from set of allowed values, assessed with `in` (Ex short for Exact Values)
    (5) Callable()                    # obj returns true with python's `callable` function
    (6) Num(<args>, num_type=<Type>)  # obj returns true if 1) is of type `num_type` and 2) lays within specified bounds in `<args>`.
    (7) Array(<shape>)                # obj of type np.ndarray, and of shape <shape> if provided
    Nesting options:  
    (A) Op(<expd1>, <expd2>)          # obj that has <expd1> or <expd2> structure
    (B) (<expd1>, <expd2>)            # Tuple (or other positional iterable) where the first element has <expd1> structure, second has <expd2> structure
    (C) (<expd>,)                     # Tuple (or other nondictlike iterable) of elements that have <expd> structure
    (D) (<expd>, <length>)            # Tuple (or other measurable iterable) of elements that have <expd> structure and integer length <length>
    (E) {<expdkey>: <expdval>}        # Dictionary (or other dictlike iterable) where keys have <expdkey> structure and values have <expdval> structure
    """
    if isinstance(info_tuple[0], str):
        info_tuple = (info_tuple,)
    for param_name, expd, actual in info_tuple:
        has_struct, struct_dict = _hasType(expd, actual)
        if not has_struct:
            error_msg = f"{param_name} must follow this structure: \n" + str(struct_dict)
            if not print_errors:
                raise TypeError(error_msg)
            else:
                print(error_msg, end="\n\n")

def _hasType(expd, actual):
    ######## Terminal options ########
    # (1) Any()
    if isinstance(expd, Any):
        has_struct = True
        struct_dict = {"Type": "Any"}
    # (2) & (3) <Type> and Op(<Type1>, <Type2>)
    elif isinstance(expd, type) or \
        (isinstance(expd, Op) and expd.allType()):
        has_struct = isinstance(actual, expd)
        struct_dict = {"Type": _stringify(expd, Op)}
    # (4) Ex("literal1", "literal2")
    elif isinstance(expd, Ex):
        has_struct = actual in expd
        struct_dict = {"Exact_Value": _stringify(expd, Ex)}
    # (5) Callable()
    elif isinstance(expd, Callable):
        has_struct = callable(actual)
        struct_dict = {"Type": "Callable"}
    # (6) Num(<inputs>)
    elif isinstance(expd, Num):
        has_struct = expd.isMatch(actual)
        struct_dict = {"Type": list(t.__name__ for t in expd.num_type)}
        if any(expd.ranges[0]):
            struct_dict["Ranges"] = expd.ranges
    # (7) Array(<shape>)
    elif isinstance(expd, Array):
        has_struct = expd.isMatch(actual)
        struct_dict = {"Type": "ndarray"}
        if expd.shape:
            struct_dict["Shape"] = expd.shape
    ######## Nesting options ########
    # (A) Op(<expd1>, <expd2>)
    elif isinstance(expd, Op):
        result_lst = tuple(map(lambda e: _hasType(e, actual), expd))
        has_struct = any(i[0] for i in result_lst)
        options_lst = list(i[1] for i in result_lst)
        struct_dict = {"Options": options_lst}
    # (B) (<expd1>, <expd2>)
    elif isinstance(expd, allowed_iters.positional) and len(expd) > 1 \
        and not any(isinstance(i, int) for i in expd):
        expd_iter = type(expd)
        if isinstance(actual, expd_iter) and len(actual) == len(expd):
            result_lst = tuple(map(lambda e, a: _hasType(e, a), expd, actual))
            has_struct = all(i[0] for i in result_lst)
        else:
            result_lst = tuple(map(lambda e, a: _hasType(e, a), expd, _Dummy(expd)))
            has_struct = False
        collection_type = expd_iter.__name__
        struct_lst = list(i[1] for i in result_lst)
        struct_dict = {"Collection": collection_type, "Structure_by_Position": struct_lst}
    # 7 & (D) (<expd>,) and (<expd>, <length>)
    elif (isinstance(expd, allowed_iters.nondictlike) and len(expd) == (1)) or \
        (isinstance(expd, allowed_iters.measurable) and len(expd) == 2 and any(isinstance(i, int) for i in expd)):
        expd_iter, expd_elem_type, length = _getExpd(expd)
        if isinstance(actual, expd_iter) and len(actual) > 0 and \
            (not length or len(actual) == length):
            result_lst = tuple(map(lambda a: _hasType(expd_elem_type, a), actual))
            has_struct = all(i[0] for i in result_lst)
        else:
            result_lst = tuple(map(lambda a: _hasType(expd_elem_type, a), _Dummy((1))))
            has_struct = False
        collection_type = expd_iter.__name__
        elem_struct = result_lst[0][1]
        struct_dict = {"Collection": collection_type, "Element_Structure": elem_struct}
        if length:
            struct_dict["Length"] = length
    # (E) {<expdkey>: <expdval>}
    elif isinstance(expd, allowed_iters.dictlike) and len(expd) == 1:
        expd_iter, expd_pair = type(expd), tuple(expd.items())[0]
        if isinstance(actual, expd_iter) and len(actual) >= 1:
            result_lst = tuple(tuple(_hasType(e, a) for e, a in zip(expd_pair, pair)) for pair in actual.items())
            has_struct = all(all(j[0] for j in i) for i in result_lst)
        else:
            result_lst = tuple(tuple(_hasType(e, a) for e, a in zip(expd_pair, pair)) for pair in _Dummy({None: None}).items())
            has_struct = False
        struct_dict = {"Collection": type(expd).__name__, "Key_Structure": result_lst[0][0][1], "Value_structure": result_lst[0][1][1]}
    else:
        raise TypeError(f"Bad structure object: {expd}")
    return (has_struct, struct_dict)
