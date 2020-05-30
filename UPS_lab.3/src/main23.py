# -*- coding: utf8 -*-
'''
Created on 24 maj 2020

@author: Krzysztof Gajewski
Zadanie przygotowane z pomocą:
- https://python-sounddevice.readthedocs.io/en/0.3.15/examples.html
- https://stackoverflow.com/questions/29832055/animated-subplots-using-matplotlib
'''
import sounddevice as sd
import soundfile as sf
import filters

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import queue

import numpy # Make sure NumPy is loaded before it is used in the process_input_data
assert numpy  # avoid "imported but unused" message (W0611)

#Zmienne, w których przechowywane będą czynniki filtrów
aNOI = []
bNOI = []
b = []

#Zmienne pomocnicze do odczytywania / zapisywania danych dźwiękowych
sine = []
buffer = []
output = []

#licznik pomocny w odczycie bieżącej pozycji z tablicy wejściowej
counter = 0
#liczba "próbek" odczytywanych / zapisywanych w pojedynczym bloku wejściowym
blocksize = 100
#domyślna częstotliwość próbkowania
samplerate= 44100
#wielkość bufora danych wejściowych / wyjściowych (2^16)
buffersize = 65536
#2^16-1 zmienna pomocnicza wykorzystywana przy operacjach bitowych
buffersizeN = buffersize-1

#kolejki wykorzystywane do aktualizacji wykresów pomocniczych
q = queue.Queue()
q2 = queue.Queue()

#zmienne pomocnicze do aktualizacji wykresów pomocniczych
downsample = 100
length = int(200 * samplerate / (1000 * downsample) )
plotdata = numpy.zeros((length, 1))
plotdata2 = numpy.zeros((length, 1))

def process_input_data(outdata, frames, time, status):
    '''
    funkcja wywoływana podczas odtwarzania próbek w karcie dźwiękowej
      - outdata - tablica, do której należy zapisać próbki, które mają zostać
        odtworzone za pomocą karty dźwiękowej
      - status - informuje o ewentualnych błędach transmisji danych  
    '''
    global counter
    if status:
        print(status)
 
    temp = []
    sine_plot = []
    output_plot = []
    
    #każda próbka "wejściowa" jest przepisywana na "wyjście"
    for i in range(blocksize):
        recentPos = (counter+i) & buffersizeN
        buffer[recentPos] = sine[recentPos]
        res = buffer[recentPos]
        output[recentPos] = res
        
        sine_plot.append([sine[recentPos][1]])
        output_plot.append([res[1]])
        temp.append(res)
    
    #Tu zapisujemy "wycinek danych", które trafiają do wyświetlenia
    q.put(sine_plot[::downsample])
    q2.put(output_plot[::downsample])

    counter = (counter + blocksize) & buffersizeN
    outdata[:] = temp

#Funkcja pomocnicza, wywoływana podczas aktualizacji wykresów pomocniczych
def update_plot(frame):
    global plotdata
    global plotdata2
    while True:
        try:
            data = q.get_nowait()
            data2 = q2.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        shift = len(data2)
        
        plotdata = numpy.roll(plotdata, -shift, axis=0)
        plotdata2 = numpy.roll(plotdata2, -shift, axis=0)
        
        plotdata[-shift:, :] = data
        plotdata2[-shift:, :] = data2

        lines[0].set_ydata(plotdata[:, 0])
        lines[1].set_ydata(plotdata2[:, 0])

    return lines

#Funkcja pomocnicza, opisująca wygląd wykresów pomocniczych pomocniczych
def setup_axes(plotdata, plotdata2, fig, ax0, ax1):
    ax0.legend(['Input'], loc='lower left', ncol=1)
    ax0.axis((0, len(plotdata), -1, 1))
    ax0.set_yticks([0])
    ax0.yaxis.grid(True)
    ax0.tick_params(bottom=False, top=False, labelbottom=False, 
        right=False, left=False, labelleft=False)
    ax1.legend(['Output'], loc='lower left', ncol=1)
    ax1.axis((0, len(plotdata2), -1, 1))
    ax1.set_yticks([0])
    ax1.yaxis.grid(True)
    ax1.tick_params(bottom=False, top=False, labelbottom=False, 
        right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

def write_sound_files():
    '''
    Funkcja pomocnicza zapisująca próbki dźwiękowe niefiltrowane (poszczególne próbki przebiegu
    sinusoidalnego) oraz próbki dźwiękowe przefiltrowane za pomocą filtru SOI lub NOI.
    Proszę dla każdego rodzaju filtru zapisać wynik filtrowania. Parametry wejściowe dla obu
    filtrów pozostawić takie same!
    W nazwie pliku proszę podać swoje imię, nazwisko, częstotliwość odcięcia filtru oraz rodzaj filtru
    według formatu:
    
    nazwisko_imie_filtr_czestotliwość_odcięcia ; np. gajewski_krzyszof_NOI_5kHz.wav  
    '''
    file = sf.SoundFile("original.wav", mode='x', samplerate=44100, channels=2)
    file.write(buffer)
    file2 = sf.SoundFile("filtered.wav", mode='x', samplerate=44100, channels=2)
    file2.write(output)

#Funkcja main realizująca logikę zadań nr 2 i 3 laboratorium 
if __name__ == '__main__':
    
    #Symulowanie "próbek wejściowych" do karty dźwiękowej
    #Przebieg sinusoidalny o określonej częstotliwości
    sine = filters.gen_sine(1000, buffersize, samplerate)
    
    #inicjalizacja buforów wejściowych
    for i in range(buffersize):
        buffer.append([0,0])
        output.append([0,0])
       
    try:
        fig, (ax0, ax1) = plt.subplots(2, 1)
        line1, = ax0.plot(plotdata)
        line2, = ax1.plot(plotdata2)
        lines = [line1, line2]
        setup_axes(plotdata, plotdata2, fig, ax0, ax1)
        
        #Aby zapisać plik "wav", proszę zakomentować poniższą linię
        ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
        with sd.OutputStream(samplerate=samplerate, blocksize=blocksize, channels=2, callback=process_input_data):
            print('#' * 80)
            print('Aby zakończyć, naciśnij Enter')
            print('#' * 80)
            #Aby zapisać plik "wav", proszę zakomentować poniższą linię
            plt.show()
            input()
            write_sound_files()
    except KeyboardInterrupt:
        exit('')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))