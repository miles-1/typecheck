from typecheck import checkType, Any, Op, Ex
import numpy as np


###########################################
#            Positive tests


checkType(
    ######## Terminal options ########
    # 1. Any()
    ("+1.0", Any(), "hello"),
    ("+1.1", Any(), 5),
    ("+1.2", Any(), None),
    ("+1.3", Any(), (("hello",),)),
    # 2. <Type>  
    ("+2.0", str, "hello"),
    ("+2.1", tuple, ("hello",)),
    ("+2.2", dict, {"hello": 1}),
    ("+2.3", int, 1),
    ("+2.4", float, 1.0),
    # 3. Op(<Type1>, <Type2>)
    ("+3.0", Op(float, int), 1),
    ("+3.1", Op(float, int), 1.0),
    ("+3.2", Op(tuple, int, float), 1),
    ("+3.3", Op(tuple, int, float), 1.0),
    ("+3.4", Op(tuple, int, float), (1.0,)),
    # 4. Ex("literal1", "literal2")
    ("+4.0", Ex("literal1", "literal2"), "literal1"),
    ("+4.1", Ex(1, "literal2", 2), 2),
    ("+4.2", Ex(None, "literal2"), None),
    ("+4.3", Ex("l", 5, 6, 7, 8, 9), 8),
    ("+4.4", Ex(1.0, (1.0,)), (1.0,)),
    ("+4.5", Ex(1, tuple), tuple),
    ("+4.6", Ex(1, tuple), 1),
    ######## Nesting options ########
    # 5. Op(<expd1>, <expd2>)
    ("+5.0", Op(float, Ex(1, 2, 3)), 1.0),
    ("+5.1", Op(float, Ex(1, 2, 3)), 2),
    ("+5.2", Op((str,), [str,1]), ("hello",)),
    ("+5.3", Op((str,), [str,1]), ["hello",]),
    # 6. (<expd1>, <expd2>)
    ("+6.0", (float, Ex(1, 2, 3)), (1.0, 2)),
    ("+6.1", [float, Ex(1, 2, 3)], [2.0, 3]),
    ("+6.2", np.array([float, Ex(1, 2, 3)], dtype=object), np.array((2.0, 3))),
    ("+6.3", (float, float, str, str), (1.0, 0.0, "5", "6")),
    ("+6.4", ((str,), [str,1]), (("hello","bye"), ["huh"])),
    # 7. (<expd>,)
    ("+7.0", (float,), (1.0, 1.5, 6.8)),
    ("+7.1", [float], [2.0, 0.3]),
    ("+7.2", {Ex(1,2,3)}, {1,3}),
    ("+7.3", np.array([float]), np.array([1.0, 5.5, 7.8, 9.9])),
    # 8. (<expd>, <length>)
    ("+8.0", (float,3), (1.0, 1.5, 6.8)),
    ("+8.1", [float,2], [2.0, 0.3]),
    ("+8.2", {Ex(1,2,3),1}, {2}),
    ("+8.3", np.array([float,4]), np.array([1.0, 5.5, 7.8, 9.9])),
    # 9. {<expdkey>: <expdval>}
    ("+9.0", {float: int}, {1.0: 2, 3.0: 5}),
    ("+9.1", {float: Ex(1,2,3)}, {1.0: 1, 3.0: 2}),
    ("+9.2", {Op(float, int): str}, {1.0: "o", 3: "t"}),
    print_errors=True
)


###########################################
#            Negative tests

checkType(
    ######## Bad expd objects ########
    # ("-0.0", {}, {1:1}),
    # ("-0.1", {tuple:str, str:int},  {"hi":1}),
    ######## Terminal options ########
    # 1. Any() should never raise error
    # 2. <Type>  
    ("-2.0", str, 1),
    ("-2.1", tuple, ["hello",]),
    ("-2.2", dict, {"hello"}),
    ("-2.3", int, 1.2),
    ("-2.4", float, "hi"),
    # 3. Op(<Type1>, <Type2>)
    ("-3.0", Op(float, int), "1"),
    ("-3.1", Op(float, int), (1,)),
    ("-3.2", Op(tuple, int, float), [3]),
    # 4. Ex("literal1", "literal2")
    ("-4.0", Ex("literal1", "literal2"), "literal"),
    ("-4.1", Ex(1, "literal2", 2), 2.1),
    ("-4.2", Ex(None, "literal2"), 5),
    ("-4.3", Ex(1.0, (1.1,)), (1.0,)),
    ######## Nesting options ########
    # 5. Op(<expd1>, <expd2>)
    ("-5.0", Op(float, Ex(1, 2, 3)), 4),
    ("-5.1", Op(float, Ex(1, 2, 3)), "4"),
    ("-5.2", Op((str,), [str,1]), (1,)),
    ("-5.3", Op((str,), [str,1]), ["hello", "bye"]),
    # 6. (<expd1>, <expd2>)
    ("-6.0", (float, Ex(1, 2, 3)), (1.0, 2, 3)),
    ("-6.1", [float, Ex(1, 2, 3)], [2, 3]),
    ("-6.2", [float, Ex(1, 2, 3)], (2.0, 3)),
    ("-6.3", np.array([float, Ex(1, 2, 3)], dtype=object), (2.0, 3)),
    ("-6.4", (float, float, str, str), (1.0, 0, "5", "6")),
    ("-6.5", (float, float, str, str), (1.0, "5", "6")),
    ("-6.6", (float, float, str, str), (1.0, "5", "6", 2, 3)),
    ("-6.7", ((str,), [str,1]), [("hello","bye"), ["huh", "ho"]]),
    # 7. (<expd>,)
    ("-7.0", (float,), (1.0, 1.5, 1)),
    ("-7.1", [float], ["1", 0.3]),
    ("-7.2", {Ex(1,2,3)}, {1,3,2.1}),
    # 8. (<expd>, <length>)
    ("-8.0", (float,3), (1.0, 1.5)),
    ("-8.1", [float,2], [2.0, 0.3, 2]),
    ("-8.2", [float,2], [2.0, 0.3, 2.0]),
    ("-8.3", {Ex(1,2,3),1}, {4}),
    ("-8.4", {Ex(1,2,3),1}, {1, 2}),
    ("-8.5", np.array([float,4]), np.array([1.0, 5.5, 7.8])),
    # 9. {<expdkey>: <expdval>}
    ("-9.0", {float: int}, {1.0: 2, 3.0: 5.0}),
    ("-9.1", {float: Ex(1,2,3)}, {1: 1, 3.0: 2}),
    ("-9.2", {float: Ex(1,2,3)}, {1.0: 4, 3.0: 2}),
    ("-9.3", {Op(float, int): str}, {1.0: "o", "3": "t"}),
    ("-9.4", {Op(float, int): str}, {1.0: "o", 4: 5}),
    print_errors=True
)