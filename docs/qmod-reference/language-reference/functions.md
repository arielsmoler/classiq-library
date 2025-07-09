# Quantum Functions

Quantum functions are operations that modify the state of quantum objects. The quantum
objects are passed to the function as arguments. In addition, quantum functions can take
classical arguments and function arguments.

The following example demonstrates how to define a simple Qmod function. Function `rotate`
applies a phase specified in pi radians to a qubit. It declares and uses a classical real-number
parameter `p` and a quantum single-qubit parameter `q`.

=== "Native"

    ```
    qfunc rotate(p: real, q: qbit) {
      PHASE(p * pi, q);
    }
    ```

=== "Python"

    ```python
    from classiq import CReal, qfunc, QBit
    from classiq.qmod.symbolic import pi


    @qfunc
    def rotate(p: CReal, qv: QBit) -> None:
        PHASE(theta=p * pi, target=qv)
    ```

## Syntax

The signature of a function comprises the function's name and its parameters, that is,
the arguments it expects when called. The function's body is the description of its
implementation as a sequence of statements.

=== "Native"

    **qfunc** _name_ **(** _parameters_ **)** **{** _statements_ **}**

    _parameters_ is a list of zero or more comma-separated declarations in one of the three forms:

    - \[ **output** | **input** \] _name_ **:** _quantum-type_
    - _name_ **:** _classical-type_
    - _name_ **:** **qfunc** [ **[** **]** ] **(** _parameters_ **)**

=== "Python"

    A quantum function is defined with a regular Python function decorated with `@qfunc`.

    The Qmod compiler extracts the signature of the quantum function from the Python type
    hints. Type hints must be specified for all parameters, and must be Qmod types or, in
    the case of classical types, their Python counterparts (see [Generative Descriptions](generative-descriptions.md)).

    Direction modifiers for quantum arguments are represented with the generic classes `Input`
    and `Output`.

## Semantics

-   A function definition introduces a new function symbol into the global namespace.
-   Parameters can be used as variables in the body of the function.
-   Classical parameters can be used as variables in the declaration of subsequent parameter
    types in the signature of the function.
-   The direction modifiers `input` and `ouput` may be used to specify input-only and
    output-only quantum parameters respectively. Note that direction modifiers cannot be used with
    classical or function parameters.

For more on Qmod types, see [Quantum Types](quantum-types.md) and [Classical Types](classical-types.md).

Qmod functions can also take functions as arguments. For details on this capability, see [Operators](operators.md).

Statements can do one of the following:

-   Call other quantum functions
-   Declare local quantum variables
-   Assign expressions to quantum variables
-   Bind quantum variables to other quantum variables

## Examples

### Example 1 - Function Declarations

The following example demonstrates function declarations:

=== "Native"

    ```
    qfunc foo(n: int, qba: qbit[2*n]) {
      // ...
    }

    qfunc bar(x: qnum, y: qnum, output res: qnum) {
      // ...
    }
    ```

=== "Python"

    ```python
    from classiq import CInt, QArray, QBit, QNum, Output, qfunc


    @qfunc
    def foo(n: CInt, qba: QArray[QBit, "2*n"]) -> None:
        pass


    @qfunc
    def bar(x: QNum, y: QNum, res: Output[QNum]) -> None:
        pass
    ```

    Note that when classical arguments are used to specify subsequent arguments, as in
    the case of `qba` being a qubit array of size 2*n, the expression is specified
    as a string literal because the Python variable `n` is not in scope.

### Example 2 - Function Definitions

The following example demonstrates a simple function definition. In its body it calls
the built-in function `H()` and then iteratively under `repeat` the function `PHASE()`
(for more on `repeat` see [Classical Control Flow](statements/classical-control-flow.md))

=== "Native"

    ```
    qfunc foo(n: int, qv: qbit) {
      H(qv);
      repeat (index: n) {
        PHASE((index / n) * pi, qv);
      }
    }
    ```

=== "Python"

    A function decorated with `@qfunc` is executed by the Python interpreter to construct
    the body of the Qmod function. Python functions corresponding to Qmod statements
    inject the respective statements into the constructed function.

    ```python
    from classiq import CInt, QBit, H, PHASE, allocate, repeat, qfunc
    from classiq.qmod.symbolic import pi


    @qfunc
    def foo(n: CInt, qv: QBit) -> None:
        H(qv)
        repeat(3, lambda i: PHASE(theta=(i / n) * pi, target=qv))
    ```
