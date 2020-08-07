from __future__ import annotations
import math
from typing import Optional, Union, TYPE_CHECKING

from ..utils import UniquelyIdentifiable, Bindable, bindable_property
# TODO: remove type checking everywhere
# Response: this is to avoid cyclic imports, I have (more) in-depth responses in some of the other files
if TYPE_CHECKING:
    from .brain import Brain


@Bindable('brain')
class Area(UniquelyIdentifiable):
    def __init__(self, n: int, k: Optional[int] = None, beta: float = 0.01):
        super(Area, self).__init__()
        self.beta: float = beta
        self.n: int = n
        self.k: int = k if k is not None else int(n ** 0.5)

        if k == 0:
            self.k = math.sqrt(n)

    # TODO: return as a set?
    @bindable_property
    def winners(self, *, brain: Brain):
        return brain.winners[self]

    @bindable_property
    def support(self, *, brain: Brain):
        return brain.support[self]

    @bindable_property
    def active_assembly(self, *, brain: Brain):
        from ..assemblies import Assembly
        return Assembly.read(self, brain=brain)

    def __repr__(self):
        return f"Area(n={self.n}, k={self.k}, beta={self.beta})"


class Stimulus(UniquelyIdentifiable):
    def __init__(self, n: int, beta: float = 0.05):
        super(Stimulus, self).__init__()
        self.n = n
        self.beta = beta

    def __repr__(self):
        return f"Stimulus(n={self.n}, beta={self.beta})"


class OutputArea(Area):
    def __init__(self, n: int, beta: float):
        super(OutputArea, self).__init__(n=n, beta=beta)

    def __repr__(self):
        return f"OutputArea(n={self.n}, beta={self.beta})"


# TODO: use a parent class instead of union
# A union is C-style code (where we would get a pointer to some place)
# It seems that there is a logical relation between the classes here, which would be better modeled using a parent class
# Response: In my opinion, this is a more specific type-hinting, and it describes exactly what is needed,
#           A parent class is less specific and will create bugs if people attempt to subclass it, no?
BrainPart = Union[Area, Stimulus]


class Connection:
    # TODO: type hinting to synapses
    # TODO 2: why is this class needed? is it well-defined? do the type hints represent what really happens in its usage?
    def __init__(self, source: BrainPart, dest: BrainPart, synapses=None):
        self.source: BrainPart = source
        self.dest: BrainPart = dest
        self.synapses = synapses if synapses is not None else {}

    @property
    def beta(self):
        # TODO: always define by dest
        if isinstance(self.source, Stimulus):
            return self.dest.beta
        return self.source.beta

    def __getitem__(self, key: int):
        return self.synapses[key]

    def __setitem__(self, key: int, value: float):
        self.synapses[key] = value

    def __repr__(self):
        return f"Connection(synapses={self.synapses!r})"