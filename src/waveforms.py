import abc
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

_LOOKUP_PATH = Path(__file__).parent.resolve() / 'note_lookup.csv'
_NOTE_2_FREQ_MAP = OrderedDict()
with open(_LOOKUP_PATH, 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        name, freq = line.strip().split(',')
        # Treat the sharp and flat spelling of a "black key" as 2 different notes
        all_names = name.split('/')
        for name in all_names:
            _NOTE_2_FREQ_MAP[name] = float(freq)

MIN_FREQUENCY = 20
MAX_FREQUENCY = 20000

note_name_to_frequency = _NOTE_2_FREQ_MAP.get


@dataclass
class SpectrumComponent:
    frequency: float
    amplitude: float = 1.0

    def closest_note(self) -> str:
        previous_distance = float('inf')
        previous_name = ''

        for name, freq in _NOTE_2_FREQ_MAP.items():
            current_distance = abs(freq - self.frequency)
            if current_distance > previous_distance:
                break
            previous_distance = current_distance
            previous_name = name

        return previous_name

    def __hash__(self):
        return 0


class WaveForm(abc.ABC):
    def __init__(self, note):
        if note not in _NOTE_2_FREQ_MAP:
            raise ValueError(f'Note "{note}" not recognised')
        self.note = note

    def __iter__(self):
        partials = self.partials
        return iter(partials)

    def __repr__(self):
        return f'{self.__class__.__name__} on {self.note}'

    @property
    @abc.abstractmethod
    def partials(self):
        pass

    def _get_partials(self, note, ignore_even, amplitude_func):
        p = []
        n = 0
        while True:
            n += 1
            if (n % 2 == 0) and ignore_even:
                continue
            frequency = note_name_to_frequency(note) * n
            if frequency > MAX_FREQUENCY:
                break
            p.append(SpectrumComponent(frequency, amplitude_func(n)))
        return p


class SineWave(WaveForm):
    @property
    def partials(self):
        return [SpectrumComponent(note_name_to_frequency(self.note), 1)]


class SawWave(WaveForm):
    @property
    def partials(self):
        return self._get_partials(
            self.note,
            ignore_even=False,
            amplitude_func=(lambda n: 1 / n),
        )


class SquareWave(WaveForm):
    @property
    def partials(self):
        return self._get_partials(
            self.note,
            ignore_even=True,
            amplitude_func=(lambda n: 1 / n),
        )


class TriangleWave(WaveForm):
    @property
    def partials(self):
        return self._get_partials(
            self.note,
            ignore_even=True,
            amplitude_func=(lambda n: 1 / n ** 2),
        )
