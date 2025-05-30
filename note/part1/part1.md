# Regex

## Zero-width match

A **zero-width match** matches a *position* where some condition is true, but does not actually capture any characters. Typical zero-width assertions are:

- `^` (start of string)
- `$` (end of string)
- `\b` (word boundary)
- `(?=...)` (lookahead)
- `(?!...)` (negative lookahead)

***

## `re.finditer()`

- Returns an iterator of `re.Match` objects, one for each match in the string.

**Example:**

```python
import re
pattern = r'\d+'  # Match one or more digits
s = "abc123def456ghi789"
matches = re.finditer(pattern, s)
for match in matches:
    print(match)         # Match object
    print(match.group()) # Matched substring
    print(match.start()) # Start position
    print(match.end())   # End position
```

**Output:**

````
<re.Match object; span=(3, 6), match='123'>
123
3
6
<re.Match object; span=(9, 12), match='456'>
456
9
12
<re.Match object; span=(15, 18), match='789'>
789
15
18
````

***

**Zero-width match example:**

```python
import re
s = "hi! bye."
matches = list(re.finditer(r'\b', s))
for m in matches:
    print(m.start(), m.group())
```

**Output:**

````
0
2
4
7
````

- For zero-width matches, `start()` returns the position ("gap") between characters, not an actual character index.
- For a *regular* match, `start()` gives the index of the first character in the matched substring.
- For a *zero-width* match, `start()` gives the "split point" between characters where the assertion holds.

***

## `re.split()`

- Splits a string wherever the pattern matches.
- If a match is at the beginning/end, you get empty strings in the result.
- Zero-width matches act as split points between characters.
- If a separator matches real characters, it consumes those characters; if not, it splits at the zero-width point.

![](1.png)

**Result:**

![](2.png)

For example, with zero-width matches:

````
['', '', 'w', 'o', 'r', 'd', 's', '', '']
````

For a pattern matching non-word characters:

```python
re.split(r'(\W*)', '...words...')
['', '...', '', '', 'w', '', 'o', '', 'r', '', 'd', '', 's', '...', '', '', '']
```

***

# Multiprocessing

## Use `fork()` to create a subprocess

```python
import os
print(f'Process {os.getpid()}')
pid = os.fork()  # Duplicates current process
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
```

***

## Use `Process` from `multiprocessing` to create a subprocess

```python
from multiprocessing import Process
import os

def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()  # Wait for child to finish
    print('Child process end.')
```

***

## Use `Pool` to manage a batch of subprocesses

```python
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(1)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(16)
    start = time.time()
    for i in range(16):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()  # No more new tasks
    p.join()   # Wait for all to finish
    end = time.time()
    print(f'All subprocesses done. time:{end - start}')
```

***

## Use `Queue` to share data between processes

```python
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

q = Queue()
pw = Process(target=write, args=(q,))
pr = Process(target=read, args=(q,))
pw.start()
pr.start()
pw.join()
pr.terminate()
```

***

# Notes on Variables and Memory in Multiprocessing

1. **Passing variables and instances**

   - Multiprocessing does *not* share memory (unlike threads). Each process has its own independent memory space.
   - Any parameters or objects you pass (including instances/methods/attributes) are **pickled and copied** for the child process.
   - If you pass an instance method, the *whole instance* is pickled and sent.
   - If you only pass function arguments, only those are pickled.

2. **Copies and Read-Only**

   - Variables/instances/attributes in a child are just *copies*. They are not kept in sync with the parent or other children.
   - The child can read them, but cannot update them for the parent.

3. **fork vs. spawn (Platform differences)**

   - **Linux fork:** The child inherits the parent’s memory (copy-on-write). At first, the child can "see" everything the parent had, but changes are not shared back.
   - **Windows/macOS spawn:** The child launches a new interpreter and re-imports the main module. The child only receives what you *explicitly* pass (by pickling); it cannot see all parent memory directly.

4. **True sharing between processes:**

   - Use `multiprocessing.Manager()`, `Value`, or `Array` to share data for real.




# Pytest

`pytest` will run all files of the form `test_*py` or `_test.py` in the current directory and its subdirectories.



**ExceptionGroup**

```py
def f():
    raise ExceptionGroup(
            'Group message',
            [
                RuntimeError(),
            ],
    )
```

`ExceptionGroup` contains moore than one exceptions. It accepts a description string and a `List[Exception]`



**Context Manager**

A class including `__enter__()` and `__exit__().` It defines what to do before and after some code.

```py
def test_exception_in_group():
    with pytest.raises(ExceptionGroup) as excinfo:
        f()
```

`pytest.raises(ExceotionGroup)` is a `Context Manager` . It would check whether a ExceptionInfo is raised, if true, store the ExceptionInfo to `excinfo`



**Group multiple tests in a class**

```py
class TestClass:
    def test_one(self):
        x = 'this'
        assert 'h' in x
    
    def test_two(self):
        x = 'hello'
        assert hasattr(x, 'check')
```



Each test has a unique instance of the class.

```py
class TestDemo:
    def test_1(self):
        self.x = 123
        assert self.x == 123

    def test_2(self):
        assert not hasattr(self, 'x')  # self.x 不存在，因为新实例
```

Above two would be passed.

```py
# content of test_class_demo.py
class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1
```

This two would not be passed.



**Request a unique temporary directory for functional tests**

```py
def test_needsfiles(tmp_path):
    print(tmp_path)
    assert 0
```

List the name `tmp_path` in the test function signature and `pytest`  will lookup and call a fixture factory to create the resorce before performing the test function all.

```bash
============================================================================================================================= test session starts =============================================================================================================================
platform linux -- Python 3.11.11, pytest-8.3.5, pluggy-1.6.0
rootdir: /home/bigorange/projects/CS336/pytest
plugins: anyio-4.8.0
collected 1 item                                                                                                                                                                                                                                                              

test_tmp_path.py F                                                                                                                                                                                                                                                      [100%]

================================================================================================================================== FAILURES ===================================================================================================================================
_______________________________________________________________________________________________________________________________ test_needsfiles _______________________________________________________________________________________________________________________________

tmp_path = PosixPath('/tmp/pytest-of-bigorange/pytest-0/test_needsfiles0')

    def test_needsfiles(tmp_path):
        print(tmp_path)
>       assert 0
E       assert 0

test_tmp_path.py:3: AssertionError
---------------------------------------------------------------------------------------------------------------------------- Captured stdout call -----------------------------------------------------------------------------------------------------------------------------
/tmp/pytest-of-bigorange/pytest-0/test_needsfiles0
=========================================================================================================================== short test summary info ===========================================================================================================================
FAILED test_tmp_path.py::test_needsfiles - assert 0
============================================================================================================================== 1 failed in 0.07s ===========
```



**Run tests by keyword expressions**

```py
class TestMyClass:
    def test_something(self):
        pass
    def test_method_simple(self):
        pass
class TestOtherClass:
    def test_method(self):
        pass
```

```bash
pytest test_keyword.py -k "TestMyClass and not test_method"
```



**Specifying a specific parametrization of a test**

```bash
pytest tests/test_mod.py::test_func[x1,y2]
```



**Run tests by marker expression**

```py
pytest -m slow
```

```bash
pytest -m slow
```



**read from a file using** **`@`** **@** **prefix**

```bash
pytest @tests_to_run.txt
```

```txt
tests/test_file.py
tests/test_mod.py::test_func[x1,y2]
tests/test_mod.py::TestClass
-m slow
```



## Fixture

When pytest goes to run a test, it looks at the parameters in that test function’s signature, and then searches for fixtures that have the same names as those parameters. Once pytest finds them, it runs those fixtures, captures what they returned (if anything), and passes those objects into the test function as arguments.

```py
import pytest


class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def cube(self):
        self.cubed = True


class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()


# Arrange
@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)
```



`fixture` marked with `@pytest.fixture(autouse=True)` would be requested automatically.

```py
# contents of test_append.py
import pytest


@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def order(first_entry):
    return []


@pytest.fixture(autouse=True)
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(order, first_entry):
    assert order == [first_entry]


def test_string_and_int(order, first_entry):
    order.append(2)
    assert order == [first_entry, 2]
```

The excuting order depends on the dependence between fixtures.

