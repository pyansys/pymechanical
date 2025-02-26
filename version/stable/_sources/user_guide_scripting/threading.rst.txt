.. _ref_mechanical_scripting_guide_threading:

Threading
=========

Concurrency and threads
-----------------------

.. note::
   The intent is not to provide an extensive explanation of concurrency and threads but
   rather to lay the groundwork for specific concurrency considerations for Mechanical's
   scripting API. Some simplifications are employed for this purpose.

CPUs can execute multiple subroutines of a program concurrently. One popular model
for this concurrency is called *threading*. There are other possible models, such
as co-routines.

A thread is a CPU virtualization of a CPU core. Traditionally, a computer can have
multiple CPUs, each executing multiple programs concurrently. Using clever scheduling,
a CPU can simulate more cores than it actually has. A thread is an abstraction around
either a CPU core executing a program or a virtual CPU core executing a program. Within
a single process, there can be multiple threads running, and these threads can be
executing in a single core or multiple cores.

In a traditional computer instruction set architecture, memory is a store of data that
stores the program itself and data used by the program. CPUs contain a small amount of
memory that can be used to run a program, but often times an external memory store,
typically using RAM, is used by the program. Frequently, when running a program, the
CPU needs to fetch data from RAM or store data back into RAM.

CPUs operate at the speed of electrons and can often do trillions of operations per
second. If there is only one program running on a CPU and a private section of memory
that the program needs, it can shuttle data to and from that memory extremely quickly.

When there are multiple programs or threads running on a CPU, things can get tricker.
Consider a (contrived) example with a simple program that increments an integer:

.. code::

    i++

If ``i`` is a 32-bit integer, it is represented in binary. For example, the number 11
is ``00000000 00000000 00000000 00001011``, and the number 12 is ``00000000 00000000 00000000 00001100``.
To change a value from 11 to 12, a total of three bits must flip between 0 and 1.
It is possible for a CPU to perform that operation with three independent bit flip instructions.

Now consider that two concurrently running threads are both trying to increment this integer
at roughly the same time, at the time scale of CPUs. The first thread flips one of
the bits, making the binary value ``00000000 00000000 00000000 00001111``, which represents the
number 15. The second thread sees that binary amount and interprets the operation to be
incrementing from 15 to 16, or from ``00000000 00000000 00000000 00001111`` to
``00000000 00000000 00000000 00010000``, which is performed using 5 bit flips. So one thread
flips the latter 3 bits, and the other thread flips the latter 5 bits. This might result in the
outcome ``00000000 00000000 00000000 00010111``, which represents the number 21, a value
certainly not two increments on the number 11. Depending on the interpretation of that integer
value by the program, the behavior of the program might do literally anything, with erratic,
random, and often difficult to reproduce (let alone fix) bugs.

Race condition
~~~~~~~~~~~~~~

This preceding situation is called a *race condition*, where concurrent programs are incorrectly
accessing or mutating the same memory in such a way that leads to surprising consequences. They may
seem rare. However, remember that when a CPU situation has a probability of one in a million, it is
likely to occur hundreds of times per second. If it has a much smaller probability than that, it can
occur once every few days or once every few weeks. In the Therac-25 radiation machine, a race
condition actually led to three deaths and more debilitating injuries.

Mitigation strategies
~~~~~~~~~~~~~~~~~~~~~

There are a number of strategies that software engineers use to benefit from the enhanced
performance of concurrent programs without suffering from race conditions:

* Data copies: Algorithms operate on private copies of data, rather than shared memory.
* Thread-compatible data structures: These data structures are designed to allow for
  concurrent read-only access of data but not concurrent write access to data.
* Thread-safe data structures: These data structures allow both concurrent read and write
  access to data.
* Task posting: All calls to a set of functions implicitly schedule the function to run on a
  dedicated thread, allowing  two calls to any of these functions to run concurrently.

Adopting any of these strategies comes with a tradeoff. Namely, these strategies typically
ask the CPU to do additional work in form of memory walls, mutexes, and other low-level
CPU-intrinsic functions. Or, they require the program to do additional work in scheduling
tasks. Usually, these are performance pessimizations for the 99% of cases where
concurrency is not needed. As such, adopting these strategies causes performance
problems for the typical user.

Mechanical's threading model
----------------------------

Mechanical is a large-scale application with multiple concurrent threads running at
any one time. However, it exhibits *thread affinity*, where a single thread is privileged above
all others with respect to data access and mutation. If the user interface (UI) is running,
this thread is typically called the UI thread, and in batch mode, it is typically called the
main thread. Some of the data structures used by Mechanical's code are thread-compatible.
Some of the APIs use task posting. However, in the general case, **using any Mechanical
API on a non-privileged thread carries a risk of race conditions**. It is difficult to quantify
the risk or to distinguish which operations are most likely to be vulnerable to them due to
the large scale of the Mechanical application's code.

As such, Mechanical APIs **MUST** only be run on the UI thread or main thread, in interactive and batch
mode respectively. For PyMechanical, this means the following:

- For an embedded instance, all scripting APIs are executed on the Python thread that constructed
  the instance of Mechanical.
- For a remote session, the Python code that is sent to the server does not contain threading
  constructs that try to run APIs in a background thread.

Given the preceding restrictions, it is possible to offload some work to a background
thread, as long as that thread does not access Mechanical's scripting API.
