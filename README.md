# Note Frequency Gaps Helper

If we know a certain collection of notes is present in an arrangement, we can sum all of their spectra to find where the "gaps" are. This may help us EQ a drum for instance, in a way that helps it stand out without masking other frequencies.

For example, if the notes C4 and Db4 are being played, there won't be harmonic content below around 250Hz, or between 300Hz and 500Hz. The "notes" being played can be modeled as sine, triangle, square, or sawtooth waves.

## Command Line Usage
Either enharmonic spelling of "black keys" is allowed (although B# won't be interpreted as C and the like)

```sh
src/note_frequency_gaps.py C4 Eb4 G4

# Or:

src/note_frequency_gaps.py C4 'D#4' G4  # Note quoting of note name containing "#"
```

## Running Tests With Coverage Check

```sh
coverage run -m unittest discover test && coverage report -m
```

View coverage results:

```sh
coverage report -m 

# Or:

coverage html && open htmlcov/index.html
```
