#!/usr/bin/env python

"""
Code to find gaps in the frequency spectrum of a given collection of notes.

Notes can be modelled by sine, triangle, square, or sawtooth waves.
"""

from dataclasses import dataclass

import matplotlib.pyplot as plt

from waveforms import MIN_FREQUENCY
from waveforms import MAX_FREQUENCY
from waveforms import SawWave
from waveforms import SineWave
from waveforms import SquareWave
from waveforms import TriangleWave


@dataclass
class SpectrumBin:
    bottom: float  # Inclusive
    top: float  # Exclusive
    magnitude: float = 0

    def contains(self, freq):
        return self.bottom <= freq < self.top

    @property
    def width(self):
        return self.top - self.bottom


def bar_graph(bins):
    plt.bar(
        [b.bottom for b in bins],
        [b.magnitude for b in bins],
        width=[b.width for b in bins],
        align='edge',
        color='blue',
        edgecolor='black',
    )
    plt.xscale('log')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()


def main(note_names, waveform_class, n_bins=100):
    """
    Build a WaveForm off of each of notes, construct a distribution, binned to closest notes, of all partials, show that and the biggest gaps
    """
    waves = [waveform_class(n) for n in note_names]

    # Binned sum over all SpectrumComponents
    bin_size = (MAX_FREQUENCY / MIN_FREQUENCY) ** (1 / n_bins)
    bin_cutoffs = [MIN_FREQUENCY]
    while True:
        next_cutoff = bin_cutoffs[-1] * bin_size
        if next_cutoff > MAX_FREQUENCY:
            break
        bin_cutoffs.append(next_cutoff)
    bin_cutoffs.append(MAX_FREQUENCY)

    bins = [
        SpectrumBin(lower, upper)
        for lower, upper in zip(bin_cutoffs, bin_cutoffs[1:])
    ]

    for wave in waves:
        for partial in wave.partials:
            for bin_ in bins:
                if bin_.contains(partial.frequency):
                    bin_.magnitude += partial.amplitude
                    break
    bar_graph([b for b in bins if b.magnitude > 0])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'note_names',
        nargs='+',
        help='names of notes whose spectra will be examined',
    )
    parser.add_argument(
        '--waveform', '-w',
        choices=('sine', 'square', 'triangle', 'saw'),
        default='saw',
        help='waveform that will be used to model notes (defaults to saw)',
    )
    args = parser.parse_args()

    waveform_class = {
        'sine': SineWave,
        'square': SquareWave,
        'triangle': TriangleWave,
        'saw': SawWave,
    }[args.waveform]

    main(args.note_names, waveform_class)
