from unittest import TestCase

from src.waveforms import *


class NoteToFrequencyTestCase(TestCase):
    def test_can_find_frequencies_for_notes(self):
        self.assertEqual(note_name_to_frequency('A4'), 440)

    def test_enharmonic_spellings_give_the_same_frequency(self):
        self.assertEqual(note_name_to_frequency('D#4'), note_name_to_frequency('Eb4'))


class SpectrumComponentTestCase(TestCase):
    def test_out_of_tune_spectrum_components_can_find_the_closest_note(self):
        self.assertEqual(SpectrumComponent(441).closest_note(), 'A4')
        
    def test_find_closest_note_when_off_the_scale(self):
        self.assertEqual(SpectrumComponent(0).closest_note(), 'C0')
        self.assertEqual(SpectrumComponent(8000).closest_note(), 'B8')


class WaveFormTestCase(TestCase):
    def test_saw_wave_is_superset_of_square_wave(self):
        saw = SawWave('A4')
        square = SquareWave('A4')
        self.assertTrue(set(saw) > set(square))

    def test_saw_wave_contains_all_freqs_found_in_itself_an_octave_higher(self):
        lower_octave_freqs = set(p.frequency for p in SawWave('A4').partials)
        upper_octave_freqs = set(p.frequency for p in SawWave('A5').partials)
        self.assertGreater(lower_octave_freqs, upper_octave_freqs)

    def test_cannot_create_waveform_from_invalid_note_name(self):
        for W in (SineWave, SquareWave, TriangleWave, SawWave):
            with self.assertRaises(ValueError):
                W(note='not a real note name')

