Compromise: Datatypes for Reasonable People
===========================================
    Should array indices start at 0 or 1? My compromise of 0.5 was rejected without, I thought, proper consideration.

    -- Stan Kelly-Bootle

In a world of disagreement, Compromise is everything for everyone. You no longer have to make the tough decisions in life.

.. code-block:: python

    >>> l = HalfIndexList('abcde')
    >>> l[0.5]
    'a'
    >>> l[1.5]
    'b'
    >>> l[-0.5]
    'e'
    >>> l.reverse()
    >>> l
    ['e', 'd', 'c', 'b', 'a']

Some may find having a set starting index a bit restrictive. They should use FlexibleList.

.. code-block:: python

    >>> l = FlexibleList('abcde')
    FlexibleList(['a', 'b', 'c', 'd', 'e'], start=0)
    >>> l.start = 5
    >>> l[7]
    'c'

SemiMutableSequences can't be changed.

.. code-block:: python

    >>> t = SemiMutableSequence(range(5))
    >>> t
    SemiMutableSequence([0, 1, 2, 3, 4])
    >>> t[1] = 7
    TypeError: SemiMutableSequence object does not support item assignment

Unless you, like, really want to.

.. code-block:: python

    >>> t = SemiMutableSequence(range(5))
    >>> try:
    ...     t[1] = 7
    ... except TypeError:
    ...     pass
    >>> t[1] = 7
    >>> t
    SemiMutableSequence([0, 7, 2, 3, 4])

But why should you be limited to a single attempt? Try a few times. If you really want mutability, you have to work for it.

.. code-block:: python

    >>> t = SemiMutableSequence(range(5), times=5)
    >>> for _ in range(4):
    ...     try:
    ...         t[1] = 7
    ...     except TypeError:
    ...         pass
    >>> t[1] = 7
    >>> t
    SemiMutableSequence([0, 7, 2, 3, 4])

Magic Numbers are bad. Who could possibly understand what this means?

.. code-block:: python

    >>> feet = yards * 3

These should be replaced by Number instances.

.. code-block:: python

    >>> from compromise import THREE
    >>> feet = yards * THREE

See? Much better. You can make longer numbers with ``&`` and floats with ``point()``

.. code-block:: python

    >>> ONE & ZERO
    10
    >>> THREE + point(ONE & FOUR)
    3.14

They're constant by convention only. Don't change them!

.. code-block:: python

    >>> TWO = (ONE & ZERO) / FOUR
    >>> TWO + TWO
    5

Or change them if you want. I don't care.
