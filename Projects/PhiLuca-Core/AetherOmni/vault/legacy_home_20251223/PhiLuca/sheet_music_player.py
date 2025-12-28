#!/usr/bin/env python3
"""
ESQET Sheet Music Player - Plays MusicXML with FluidSynth + SoundFont
Supports symphony renders (FCU Arpeggio, ER=EPR Bridge, etc.)
"""
import os
import sys
import time
from pathlib import Path
from music21 import converter

import fluidsynth

# === CONFIGURATION ===
DEFAULT_SOUNDFONT = str(Path.home() / "GeneralUser_GS_v1.471.sf2")
DEFAULT_XML = "esqet_uift_symphony.musicxml"

def play_musicxml(xml_path: str, soundfont_path: str):
    if not Path(xml_path).exists():
        print(f"Error: MusicXML file not found: {xml_path}")
        print("Generate it first with your score generator.")
        return

    if not Path(soundfont_path).exists():
        print(f"Error: SoundFont not found: {soundfont_path}")
        print("Download GeneralUser GS v1.471.sf2 and place it in your home folder.")
        return

    print(f"Loading {xml_path}...")
    score = converter.parse(xml_path)
    print(f"Title: {score.metadata.title or 'ESQET Symphony'}")

    print("Initializing FluidSynth synthesizer...")
    fs = fluidsynth.Synth(gain=1.0)
    fs.start(driver="portaudio")  # Use 'alsa' on Linux if needed

    sfid = fs.sfload(soundfont_path)
    fs.program_select(0, sfid, 0, 0)  # Channel 0, default piano (will override per part later)

    print("Playing symphony...")
    for element in score.recurse().notesAndRests:
        if element.isNote:
            midi_num = element.pitch.midi
            velocity = int(element.volume.realized * 127) if element.volume.realized else 90
            fs.noteon(0, midi_num, velocity)
            duration = element.duration.quarterLength * 0.5  # Base tempo ~120 BPM
            time.sleep(duration)
            fs.noteoff(0, midi_num)
        elif element.isChord:
            velocity = 100
            for p in element.pitches:
                fs.noteon(0, p.midi, velocity)
            duration = element.duration.quarterLength * 0.5
            time.sleep(duration)
            for p in element.pitches:
                fs.noteoff(0, p.midi)
        else:  # Rest
            time.sleep(element.duration.quarterLength * 0.5)

    fs.delete()
    print("Performance complete. Φ-coherence sustained.")

if __name__ == "__main__":
    xml_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_XML
    sf_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_SOUNDFONT
    play_musicxml(xml_file, sf_file)
