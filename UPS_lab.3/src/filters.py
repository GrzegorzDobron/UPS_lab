import math

M = 0

def gen_sine(f, N, samplerate):
    '''
    Funkcja służąca do wygenerowania przebiegu sinusoidalnego o zadanej 
    częstotliwości.
    Parametry wejściowe:
      - f - częstotliwość generowanego sinusa
      - N - liczba generowanych próbek 
      - samplerate - częstotlwość próbkowania (liczba próbek/sekundę)
    Zwracany wynik:
      - tablica wygenerowanych próbek gotowa do przesłania do karty dźwiękowej. 
        Pojedyncza próbka składa się z danych dla dwóch kanałów wyjściowych
    '''
    y = []
    bufLen = N
    for i in range(bufLen):
        sample = math.sin(2*math.pi*f*i/samplerate)
        y.append([sample, sample])
    return y

def IIR4th(fs, fc):
    '''
    Funkcja wyliczająca współczynniki filtru NOI.
    Parametry wejściowe:
      - fs - częstotliwość próbkowania
      - fc - częstotliwość odcięcia filtru 
    Zwracany wynik:
      - tablica zawierająca tablice współczynników a i b filtru NOI
    '''
    a = [0, 0, 0, 0, 0]
    b = [0, 0, 0, 0, 0]
    a1 = [0, 0, 0]
    a2 = [0, 0, 0]
    b1 = [0, 0, 0]
    b2 = [0, 0, 0]
    
    K= 2 * fs
    wc = 2 * math.pi * fc 
    c = wc * wc
    d = -2.0 * wc * math.cos(math.pi * 5.0 / 8.0)
    MM = K * K + d * K + c
    
    b1[0] = c / MM
    b1[1] = 2 * c / MM
    b1[2] = c / MM
    a1[0] = 1 
    a1[1] = (2 * c - 2 * K * K) / MM
    a1[2] = (K * K - d * K + c) / MM

    d = -2.0 * wc * math.cos(math.pi * 7.0 / 8.0)
    MM = K * K + d * K + c
    
    b2[0] = c / MM
    b2[1] = 2 * c / MM
    b2[2] = c / MM
    a2[0] = 1
    a2[1] = (2 * c - 2 * K * K) / MM
    a2[2] = (K * K - d * K + c) / MM
    
    for i in range(3):
        for j in range(3):
            a[i+j]+=a1[i]*a2[j]
            b[i+j]+=b1[i]*b2[j]
            
    return [a, b]

def sinc_filter(fs, fc, N):

    i = 0
    h = (N-1) >> 1
    f0 = fc / fs
    s=0
    b = []
    for i in range(N):
        b.append(0)

    for i in range(N):
        b[i] = 0.42 - 0.5 * math.cos(2*math.pi * i / (N-1)) + 0.08 * math.cos(4 * math.pi * i / (N-1))
        if( i == h):
            b[i] *= 1.0
        else:
            b[i] *= math.sin(2.0 * math.pi * (i-h) * f0) / 2.0 / math.pi / f0 / (i-h)
        s += b[i]

    for i in range(N):
        b[i] /= s

    return b

def FIR(bufor_we, recent_pos, b):

    temp = [0,0]
    for x in range(len(b)):
        temp[0] = temp[0] + ((bufor_we[(recent_pos - x)][0]) * b[x&(len(b)-1)])
        #print(bufor_we[(recent_pos - x)][0])
    temp[1] = temp[0]
    return temp

def IIR(bufor_we, bufor_wy, recent_pos, y_pos, a, b):

    temp = [0, 0]
    for x in range(len(a)):
        temp[0] = temp[0] + ((bufor_we[(recent_pos - x)][0]) * a[x & (len(a) - 1)])
    for x in range(len(b)):
        temp[0] = temp[0] - ((bufor_wy[(recent_pos - x)][0]) * b[x & (len(b) - 1)])
    temp[1] = temp[0]
    return temp

def echo(bufor, element, recent_pos, echo_num):

    element[0] = element[0]
    element[1] = (bufor[recent_pos-echo_num][1]*0.2 + element[1] *0.8)
    return element