import pygame
import wave
import math
import numpy as np

def main():


    # two pulse wave generators, a triangle wave, noise, and a delta modulation channel


    wave = sine_wave()


    print("Done!")

main()

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    return (float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i)/float(framerate))) for i in range(0))