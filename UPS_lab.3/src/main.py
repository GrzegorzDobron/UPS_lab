import  sounddevice as sd
import  soundfile   as sf
import  numpy
from    filters import echo
assert  numpy

buffer          = []                # Zmienna pomocnicza do zapisywania danych dźwiękowych
counter         = 0                 # licznik pomocny w odczycie bieżącej pozycji z tablicy wejściowej
bufor_position  = 0                 # pozycja bufora
blocksize       = 10                # liczba "próbek" odczytywanych / zapisywanych w pojedynczym bloku wejściowym
samplerate      = 44100             # domyślna częstotliwość próbkowania
buffersize      = 65536             # wielkość bufora danych wejściowych / wyjściowych (2^16)
buffersizeN     = buffersize - 1    # 2^16-1 zmienna pomocnicza wykorzystywana przy operacjach bitowych
channels        = 2                 # Liczba kanałów (2 - lewy prawy)
echo_parametr   = 15000             # parametr określający 'przesuniecie'echa

def bufor_operation(bufor, indata):

    global bufor_position
    bufor_position = bufor_position + 1
    if bufor_position > buffersizeN:
        bufor_position = 0
    bufor[bufor_position][0] = indata[0]
    bufor[bufor_position][1] = indata[1]

    return bufor

def process_input_data(indata, outdata, frames, time, status):

    global buffer, bufor_position
    if status:
        print(status)
    temp = []
    for i in range(blocksize):
        buffer = bufor_operation(buffer, indata[i])
        out = echo(buffer, indata[i], bufor_position, echo_parametr)
        temp.append(out)

    outdata[:] = temp

def write_sound_files():

    out_file = []
    for i in range(buffersize):
        out_file.append(bufot_out[(counter + i) & buffersizeN])
    file = sf.SoundFile("echo.wav", mode='x', samplerate=samplerate, channels=channels)
    print(out_file)
    file.write(out_file)

if __name__ == '__main__':

    for i in range(buffersize):
      buffer.append([0, 0])

    try:
        with sd.Stream(samplerate=samplerate, blocksize=blocksize, channels=channels, callback=process_input_data):
            print('#' * 80)
            print('Aby zakończyć, naciśnij Enter')
            print('#' * 80)
            input()
            write_sound_files()
    except KeyboardInterrupt:
        exit('')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))