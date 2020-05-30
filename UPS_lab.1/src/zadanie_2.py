"""
import bibliotek
"""
import soundcard as sc
import numpy as np
import wave


"""
zapis do pliku
"""
def write_sound(data, filename):
    file = wave.open(filename, 'w')
    file.setnchannels(1)
    file.setsampwidth(2)
    file.setframerate(95000)
    file.writeframesraw(convert_sound_data(data))
    file.close() 

"""
konwersja tablicy data
"""
def convert_sound_data(data):
    max_amplitude = 2**15-1
    data = max_amplitude*data
    data = data.astype(np.int16).tostring()
    return data

speakers = sc.all_speakers()
default_speaker = sc.default_speaker()

mics = sc.all_microphones()
default_mic = sc.default_microphone()

amp = 100                       #wzmocnienie
samplerate = 48000              #f_probkowania
channels = 2
numframes = 150000              #liczba_probek

chanel_left = np.array([[1, 0]])
chanel_right = np.array([[0, 1]])

print (default_mic)
print (default_speaker)

print('start nagrywania \n')
data = default_mic.record(samplerate=samplerate, channels=channels, numframes=numframes)
print('koniec nagrywania \n')

print('sygnał surowy \n', np.array(data), '\n')
print('sygnal wzmocniony \n', np.array(data*amp))

default_speaker.play(data, channels=2, samplerate=samplerate)
default_speaker.play(np.array(data*amp), channels=2, samplerate=samplerate)
default_speaker.play(np.array(data*amp*chanel_left), channels=2, samplerate=samplerate)
default_speaker.play(np.array(data*amp*chanel_right), channels=2, samplerate=samplerate)

write_sound(data, 'surowy.wav')   #wywołanie_funkcji_zapis_do_pliku
print('\nplik surowy.wav zapisany \n')
write_sound(np.array(data*amp), 'wzmocniony.wav')   #wywołanie_funkcji_zapis_do_pliku
print('plik wzmocniony.wav zapisany \n')
write_sound(np.array(data*chanel_left), 'lewy.wav')   #wywołanie_funkcji_zapis_do_pliku
print('plik lewy.wav zapisany \n')
write_sound(np.array(data*chanel_right), 'prawy.wav')   #wywołanie_funkcji_zapis_do_pliku
print('plik prawy.wev zapisany \n')


