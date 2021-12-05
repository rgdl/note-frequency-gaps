# Note Frequency Gaps Helper

If we know a certain collection of notes is present in an arrangement, we can sum all of their spectra to find where the "gaps" are. This may help us EQ a drum for instance, in a way that helps it stand out without masking other frequencies.

# TODO: give a concrete example with specific notes/frequencies
# TODO: are there other uses?

## Command Line Usage
Either enharmonic spelling of "black keys" is allowed (although B# won't be interpreted as C and the like)
```sh
src/note_frequency_gaps.py C4 Eb4 G4
```
Or:
```sh
src/note_frequency_gaps.py C4 D#4 G4
```

## Running Tests
```sh
python -m unittest discover test
```
