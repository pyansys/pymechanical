Create a pool of Mechanical servers
===================================

The `LocalMechanicalPool <../api/ansys/mechanical/core/pool/LocalMechanicalPool.html>`_
class simplifies creating and connecting to multiple servers of the
`Mechanical <../api/ansys/mechanical/core/mechanical/Mechanical.html>`_ class for batch
processing. You can use this class for batch processing a set of input files or
other batch-related processes.

This code shows how to create a pool with 10 instances:

.. code:: pycon

    >>> from ansys.mechanical.core import LocalMechanicalPool
    >>> pool = LocalMechanicalPool(10, version="251")
    'Mechanical Pool with 10 active instances'

When you are creating a pool, you can supply additional keyword arguments.
For example, to restart failed instances, you can set ``restart_failed=True``:

.. code:: pycon

    >>> import os
    >>> my_path = os.getcmd()
    >>> pool = LocalMechanicalPool(10, version="251", restart_failed=True)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

You can access each individual instance of Mechanical with this code:

.. code:: pycon

    >>> pool[0]
    <ansys.mechanical.core.mechanical.Mechanical at 0x7fabf0230d90>

Because this is a *self-healing pool*, if an instance of Mechanical stops
during a batch process, this instance is automatically restarted. When creating
the pool, you can disable this behavior by setting ``restart_failed=False``.

Run a set of input files
------------------------

You can use the pool to run a set of pre-generated input files using the
`run_batch() <../api/ansys/mechanical/core/pool/LocalMechanicalPool.html#LocalMechanicalPool.run_batch>`_ method.

For example, you can run the first set of 20 verification files with this code:

.. code:: pycon

     >>>>>> from ansys.mechanical.core import examples
     >>> files = [f"test{index}.py" for index in range(1, 21)]
     >>> outputs = pool.run_batch(files)
     >>> len(outputs)
     20

Run a user-defined function
---------------------------

While the previous example uses the `run_batch()`_
method to run a set of inputs files, you can also use the
`map() <../api/ansys/mechanical/core/pool/LocalMechanicalPool.html#LocalMechanicalPool.map>`_ method to run a custom user-defined function on
each instance of Mechanical over a set of input files.

.. code:: pycon

    >>> completed_indices = []
    >>> def func(mechanical, input_file, index):
    ...     # input_file, index = args
    ...     mechanical.clear()
    ...     output = mechanical.run_python_script_from_file(input_file)
    ...     completed_indices.append(index)
    ...     return output
    ...
    >>> inputs = [("test{index}.py", i) for i in range(1, 10)]
    >>> output = pool.map(func, inputs, progress_bar=True, wait=True)
    ['result1',
     'result2',
     'result3',
     'result4',
     'result5',
     'result6',
     'result7',
     'result8',
     'result9']
