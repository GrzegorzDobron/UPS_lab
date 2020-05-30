import sounddevice as sd
import soundfile as sf
import filters
import numpy  # Make sure NumPy is loaded before it is used in the process_input_data
assert numpy  # avoid "imported but unused" message (W0611)

buffer = []                     #Zmienna pomocnicza do zapisywania danych dźwiękowych
counter = 0                     #licznik pomocny w odczycie bieżącej pozycji z tablicy wejściowej
blocksize = 10                  #liczba "próbek" odczytywanych / zapisywanych w pojedynczym bloku wejściowym
samplerate= 44100               #domyślna częstotliwość próbkowania
buffersize = 65536              #wielkość bufora danych wejściowych / wyjściowych (2^16)
buffersizeN = buffersize-1      #2^16-1 zmienna pomocnicza wykorzystywana przy operacjach bitowych

def process_input_data(indata, outdata, frames, time, status):

    '''
    funkcja wywoływana podczas odtwarzania próbek w karcie dźwiękowej
      - indata - tablica próbek wejściowych, które należy przetworzyć, aby 
        zrealizować funkcję echo
      - outdata - tablica, do której należy zapisać próbki, które mają zostać
        odtworzone za pomocą karty dźwiękowej
      - status - informuje o ewentualnych błędach transmisji danych  
    '''

    global counter
    if status:
        print(status)
 
    temp = []
    for i in range(blocksize):
        res = indata[i]
        temp.append(res)
    counter = (counter + blocksize) & buffersizeN

    outdata[:] = temp

def write_sound_files():

    #nazwisko_imie_echo ; np. gajewski_krzyszof_echo.wav

    out_file = []
    for i in range(buffersize):
        out_file.append(buffer[(counter + i) & buffersizeN])
    file = sf.SoundFile("gd_echo.wav", mode='x', samplerate=44100, channels=2)
    file.write(out_file)



if __name__ == '__main__':
    '''
    for i in range(buffersize):
        buffer.append([0,0])
    '''
    try:
        with sd.Stream(samplerate=samplerate, blocksize=blocksize, channels=2, callback=process_input_data):
            print('#' * 80)
            print('Aby zakończyć, naciśnij Enter')
            print('#' * 80)
            input()
            write_sound_files()
    except KeyboardInterrupt:
        exit('koniec programu')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))