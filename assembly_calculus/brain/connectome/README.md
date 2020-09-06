A connectome represents the graph of connections between areas and stimuli of the brain.

A connectome is initialized with a list of areas and stimuli,
and `p` = the probability of a connection between 2 neurons.

For example:

```python
from brain.connectome import *
from brain.components import Area, Stimulus
def simple_conn():
    a = Area(n=2, k=1, beta=0.2)
    b = Area(n=2, k=1, beta=0.2)
    s = Stimulus(n=1, beta=0.2)
    return Connectome(p=0.3, areas=[a,b], stimuli=[s], initialize=True), a, b, s
```

`initialize=True` will initialize the given areas and stimuli connections.

One my also add areas and or stimuli after creating a connectome, like so:

```python
>>> conn.add_area(a)
>>> conn.add_stimulus(s)
```

After initializing a connectome,
one may fire the connectome from given sources to given destinations.

For example:

```python
>>> conn, a, b, s = simple_conn()
>>> conn.fire({s: [a], a: [b]})
```

This will cause a projection from `s` to `a` and from `a` to `b`.