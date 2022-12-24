from typecheck import checkType, Any, Op, Ex, Callable, Num, Array
import numpy as np


###########################################
#            Positive tests


checkType(
    ######## Terminal options ########
    # (1) Any()
    ("+1.0", Any(), "hello"),
    ("+1.1", Any(), 5),
    ("+1.2", Any(), None),
    ("+1.3", Any(), (("hello",),)),
    # (2) <Type>  
    ("+2.0", str, "hello"),
    ("+2.1", tuple, ("hello",)),
    ("+2.2", dict, {"hello": 1}),
    ("+2.3", int, 1),
    ("+2.4", float, 1.0),
    # (3) Op(<Type1>, <Type2>)
    ("+3.0", Op(float, int), 1),
    ("+3.1", Op(float, int), 1.0),
    ("+3.2", Op(tuple, int, float), 1),
    ("+3.3", Op(tuple, int, float), 1.0),
    ("+3.4", Op(tuple, int, float), (1.0,)),
    # (4) Ex("literal1", "literal2")
    ("+4.0", Ex("literal1", "literal2"), "literal1"),
    ("+4.1", Ex(1, "literal2", 2), 2),
    ("+4.2", Ex(None, "literal2"), None),
    ("+4.3", Ex("l", 5, 6, 7, 8, 9), 8),
    ("+4.4", Ex(1.0, (1.0,)), (1.0,)),
    ("+4.5", Ex(1, tuple), tuple),
    ("+4.6", Ex(1, tuple), 1),
    # (5) Callable()
    ("+5.0", Callable(), isinstance),
    ("+5.1", Callable(), str),
    # (6) Num(<args>, num_type=<Type>)
    ("+6.0", Num(None, 5), 1.0),
    ("+6.1", Num(2, 5, num_type=float), 2.0),
    ("+6.2", Num(2, 5, num_type=int), 5),
    ("+6.3", Num(5, None), 8),
    ("+6.4", Num((1,2), (3,4), (5, None)), 1.5),
    ("+6.5", Num((1,2), (3,4), (5, None)), 4),
    ("+6.6", Num((1,2), (3,4), (5, None)), 5),
    ("+6.7", Num((1,2), (3,4), (5, None)), 20),
    ("+6.8", Num((1,2), (3,4), (5, None)), 10**100),
    # (7) Array(<shape>)
    ("+7.0", Array(), np.array([1,2])),
    ("+7.1", Array(), np.array([[1,2],[3,4]])),
    ("+7.2", Array(2), np.array([1,2])),
    ("+7.3", Array(2, 2), np.array([[1,2],[3,4]])),
    ("+7.4", Array(2, 2, 3), np.array([[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]]])),
    ######## Nesting options ########
    # (A) Op(<expd1>, <expd2>)
    ("+A.0", Op(float, Ex(1, 2, 3)), 1.0),
    ("+A.1", Op(float, Ex(1, 2, 3)), 2),
    ("+A.2", Op((str,), [str,1]), ("hello",)),
    ("+A.3", Op((str,), [str,1]), ["hello",]),
    # (B) (<expd1>, <expd2>)
    ("+B.0", (float, Ex(1, 2, 3)), (1.0, 2)),
    ("+B.1", [float, Ex(1, 2, 3)], [2.0, 3]),
    ("+B.2", np.array([float, Ex(1, 2, 3)], dtype=object), np.array((2.0, 3))),
    ("+B.3", (float, float, str, str), (1.0, 0.0, "5", "6")),
    ("+B.4", ((str,), [str,1]), (("hello","bye"), ["huh"])),
    # (C) (<expd>,)
    ("+C.0", (float,), (1.0, 1.5, 1.8)),
    ("+C.1", [float], [2.0, 0.3]),
    ("+C.2", {Ex(1,2,3)}, {1,3}),
    ("+C.3", np.array([float]), np.array([1.0, 6.5, 3.8, 1.9])),
    # (D) (<expd>, <length>)
    ("+D.0", (float,3), (1.0, 1.5, 6.8)),
    ("+D.1", [float,2], [2.0, 0.3]),
    ("+D.2", {Ex(1,2,3),1}, {2}),
    ("+D.3", np.array([float,4]), np.array([1.0, 3.5, 2.8, 1.9])),
    # (E) {<expdkey>: <expdval>}
    ("+E.0", {float: int}, {1.0: 2, 3.0: 5}),
    ("+E.1", {float: Ex(1,2,3)}, {1.0: 1, 3.0: 2}),
    ("+E.2", {Op(float, int): str}, {1.0: "o", 3: "t"}),
    print_errors=True
)


###########################################
#            Negative tests

checkType(
    ######## Bad expd objects ########
    # ("-0.0", {}, {1:1}),
    # ("-0.1", {tuple:str, str:int},  {"hi":1}),
    ######## Terminal options ########
    # (1) Any() should never raise error
    # (2) <Type>  
    ("-2.0", str, 1),
    ("-2.1", tuple, ["hello",]),
    ("-2.2", dict, {"hello"}),
    ("-2.3", int, 1.2),
    ("-2.4", float, "hi"),
    # (3) Op(<Type1>, <Type2>)
    ("-3.0", Op(float, int), "1"),
    ("-3.1", Op(float, int), (1,)),
    ("-3.2", Op(tuple, int, float), [3]),
    # (4) Ex("literal1", "literal2")
    ("-4.0", Ex("literal1", "literal2"), "literal"),
    ("-4.1", Ex(1, "literal2", 2), 2.1),
    ("-4.2", Ex(None, "literal2"), 5),
    ("-4.3", Ex(1.0, (1.1,)), (1.0,)),
    # (5) Callable()
    ("-5.0", Callable(), 1),
    ("-5.1", Callable(), "hello"),
    # (6) Num(<args>, num_type=<Type>)
    ("-6.0", Num(None, 5), "hello"),
    ("-6.1", Num(None, 5), 5.01),
    ("-6.2", Num(2, 5), 1),
    ("-6.3", Num(2, 5, num_type=float), 6.0),
    ("-6.4", Num(5, None), 4.9),
    ("-6.5", Num((1,2), (3,4), (5, None)), 0.5),
    ("-6.6", Num((1,2), (3,4), (5, None)), 2.6),
    ("-6.7", Num((1,2), (3,4), (5, None)), 4.9),
    ("-6.8", Num((1,2), (3,4), (5, None)), -1),
    # (7) Array(<shape>)
    ("-7.0", Array(), 1),
    ("-7.1", Array(), [1,2]),
    ("-7.2", Array(), (1,2,3)),
    ("-7.3", Array(2), np.array([1,2,3])),
    ("-7.4", Array(2), np.array([[1,2],[2,3],[3,4]])),
    ("-7.5", Array(2, 1), np.array([[1,2],[3,4]])),
    ("-7.6", Array(2, 2), np.array([[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]]])),
    ######## Nesting options ########
    # (A) Op(<expd1>, <expd2>)
    ("-A.0", Op(float, Ex(1, 2, 3)), 4),
    ("-A.1", Op(float, Ex(1, 2, 3)), "4"),
    ("-A.2", Op((str,), [str,1]), (1,)),
    ("-A.3", Op((str,), [str,1]), ["hello", "bye"]),
    # (B) (<expd1>, <expd2>)
    ("-B.0", (float, Ex(1, 2, 3)), (1.0, 2, 3)),
    ("-B.1", [float, Ex(1, 2, 3)], [2, 3]),
    ("-B.2", [float, Ex(1, 2, 3)], (2.0, 3)),
    ("-B.3", np.array([float, Ex(1, 2, 3)], dtype=object), (2.0, 3)),
    ("-B.4", (float, float, str, str), (1.0, 0, "5", "6")),
    ("-B.5", (float, float, str, str), (1.0, "5", "6")),
    ("-B.6", (float, float, str, str), (1.0, "5", "6", 2, 3)),
    ("-B.7", ((str,), [str,1]), [("hello","bye"), ["huh", "ho"]]),
    # (C) (<expd>,)
    ("-C.0", (float,), (1.0, 1.5, 1)),
    ("-C.1", [float], ["1", 0.3]),
    ("-C.2", {Ex(1,2,3)}, {1,3,2.1}),
    # (D) (<expd>, <length>)
    ("-D.0", (float,3), (1.0, 1.5)),
    ("-D.1", [float,2], [2.0, 0.3, 2]),
    ("-D.2", [float,2], [2.0, 0.3, 2.0]),
    ("-D.3", {Ex(1,2,3),1}, {4}),
    ("-D.4", {Ex(1,2,3),1}, {1, 2}),
    ("-D.5", np.array([float,4]), np.array([1.0, 1.5, 0.8])),
    # (E) {<expdkey>: <expdval>}
    ("-E.0", {float: int}, {1.0: 2, 3.0: 1.0}),
    ("-E.1", {float: Ex(1,2,3)}, {1: 1, 3.0: 2}),
    ("-E.2", {float: Ex(1,2,3)}, {1.0: 4, 3.0: 2}),
    ("-E.3", {Op(float, int): str}, {1.0: "o", "3": "t"}),
    ("-E.4", {Op(float, int): str}, {1.0: "o", 4: 5}),
    print_errors=True
)