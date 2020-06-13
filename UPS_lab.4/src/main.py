import sounddevice as sd
import soundfile as sf
import generator

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import queue

import numpy # Make sure NumPy is loaded before it is used in the process_input_data
assert numpy

sine = []
buffer = []
output = []

counter     = 0                 #licznik pomocny w odczycie bieżącej pozycji z tablicy wejściowej
blocksize   = 100               #liczba "próbek" odczytywanych / zapisywanych w pojedynczym bloku wejściowym
samplerate  = 44100             #domyślna częstotliwość próbkowania
buffersize  = 65536             #wielkość bufora danych wejściowych / wyjściowych (2^16)
buffersizeN = buffersize-1      #2^16-1 zmienna pomocnicza wykorzystywana przy operacjach bitowych
q = queue.Queue()               #kolejki wykorzystywane do aktualizacji wykresów pomocniczych

#zmienne pomocnicze do aktualizacji wykresów pomocniczych
downsample = 100
length = int(200 * samplerate / (1000 * downsample) )
plotdata = numpy.zeros((length, 1))

#Zamienić komentarze, aby wykonać zadanie nr 3
def process_input_data(outdata, frames, time, status):
#def process_input_data(indata, outdata, frames, time, status):
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
    output_plot = []
    
    #każda próbka "wejściowa" jest przepisywana na "wyjście"
    for i in range(blocksize):
        recentPos = (counter+i) & buffersizeN

        right = recht.LUT_generator()
        left = links.LUT_generator()

        buffer[recentPos] = [left, right] #do aktualnej pozycji bufora wrzuć dwuelementowy zestaw próbek
        buffer[recentPos] = data[recentPos]
        res = buffer[recentPos]
        
        output_plot.append([res[1]])
        temp.append(res)
    
    #Tu zapisujemy "wycinek danych", które trafiają do wyświetlenia
    q.put(output_plot[::downsample])

    counter = (counter + blocksize) & buffersizeN
    outdata[:] = temp

#Funkcja pomocnicza, wywoływana podczas aktualizacji wykresów pomocniczych
def update_plot(frame):
    global plotdata
    global plotdata2
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        
        shift = len(data)
        plotdata = numpy.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
        line[0].set_ydata(plotdata[:, 0])

    return line

#Funkcja pomocnicza, opisująca wygląd wykresów pomocniczych pomocniczych
def setup_axes(plotdata, fig, ax0):
    ax0.legend(['Output'], loc='lower left', ncol=1)
    ax0.axis((0, len(plotdata), -1, 1))
    ax0.set_yticks([0])
    ax0.yaxis.grid(True)
    ax0.tick_params(bottom=False, top=False, labelbottom=False, 
        right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

def write_sound_files():
    '''
    Funkcja pomocnicza zapisująca próbki dźwiękowe wygenerowane przez studenta.
    Proszę zapisać 2 - 3 pliki dźwiękowe wygenerowane za pomocą funkcji LUT_generator,
    jak i NOI_generator.
    W nazwie pliku proszę podać swoje imię, nazwisko, częstotliwość wygenerowanej 
    sinusoidy oraz rodzaj użytej funckji według formatu:
    
    nazwisko_imie_czestotliwość_rodzaj_funkcji_generującej ; 
    np. gajewski_krzyszof_159_5Hz_noi_generator.wav  
    '''
    file = sf.SoundFile("generator.wav", mode='x', samplerate=44100, channels=2)
    file.write(buffer)

#Funkcja main realizująca logikę zadań nr 2 i 3 laboratorium 
if __name__ == '__main__':

    links = LutGenerator()
    links.reset_LUT_generator(fs = samplerate, fsin = 10000, fi = 0)
    recht = LutGenerator()
    recht.reset_LUT_generator(fs = samplerate, fsin = 10000, fi = 90)

    data, fs = sf.read("..\\resources\\sinus_10kHz.wav", dtype='float32')
        
    for i in range(buffersize):
        buffer.append([0,0])
        output.append([0,0])
       
    try:
        fig, ax0 = plt.subplots()
        line = ax0.plot(plotdata)
        setup_axes(plotdata, fig, ax0)
        
        #Aby zapisać plik "wav", proszę zakomentować poniższą linię
        ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
        
        with sd.OutputStream(samplerate=samplerate, blocksize=blocksize, channels=2, callback=process_input_data):
        #with sd.Stream(samplerate=samplerate, blocksize=blocksize, channels=2, callback=process_input_data):
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