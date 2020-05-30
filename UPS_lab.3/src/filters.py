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
    '''
    Funkcja wyliczająca współczynniki filtru SOI.
    Parametry wejściowe:
      - fs - częstotliwość próbkowania
      - fc - częstotliwość odcięcia filtru
      - N  - długość odpowiedzi filtru NOI  
    Zwracany wynik:
      - tablica zawierająca współczynniki b filtru SOI
    '''
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
    '''
    Funkcja realizująca filtrację SOI w czasie rzeczywistym. Funkcja ta jest 
    do zaimplementowania w zadaniu nr 2. Parametry wejściowe:
      - bufor we - bufor danych zawierający dane do przefiltrowania
      - recent_pos - indeks bieżącej próbki w buforze wejściowym, którą należy
        przetworzyć
      - b - współczynniki filtru SOI
    Zwracany wynik:
      - wynik przetwarzania bieżącej próbki w formacie gotowym do przekazania 
        do karty dźwiękowej
      
    UWAGA: 
      Wszelkie operacje wykonane na buforze wejściowym w będą widoczne poza 
      funkcją.
    '''
    return [0, 0]

def IIR(bufor_we, bufor_wy, recent_pos, y_pos, a, b):
    '''
    Funkcja realizująca filtrację NOI w czasie rzeczywistym. Funkcja ta jest 
    do zaimplementowania w zadaniu nr 3. Parametry wejściowe:
      - bufor we - bufor danych zawierający dane do przefiltrowania
      - bufor wy - bufor danych zawierający dane przefiltrowane
      - recent_pos - indeks bieżącej próbki w buforze wejściowym, którą należy
        przetworzyć
      - y_pos - indeks bieżącej próbki w buforze wyjściowym
        UWAGA: w obecnym laboratorium przyjęto, że bufor wejściowy ma tą samą 
        wielkość, co bufor wyjściowy. W ogólności te dwie wielkości mogą być 
        różne
      - a / b - współczynniki filtru NOI
      
    Zwracany wynik:
      - wynik przetwarzania bieżącej próbki w formacie gotowym do przekazania 
        do karty dźwiękowej
      
    UWAGA: 
      Wszelkie operacje wykonane na buforze wejściowym i wyjściowym w będą 
      widoczne poza funkcją.
    '''
    return [0, 0]

def echo(bufor, element, recent_pos, echo_num):
    '''
    Funkcja realizująca echo. Funkcja ta jest do zaimplementowania 
    w zadaniu nr 1. 
    Parametry wejściowe:
      - bufor - bufor zawierający przetworzone próbki echa
      - element - bieżący element do przetworzenia i do wstawienia do tablicy danych przetworzonych
      - recent_pos - indeks bieżącej pozycji do zapisania w buforze
      - echo_num - wielkość "przesunięcia" echa
    Zwracany wynik:
      - wynik przetwarzania bieżącej próbki w formacie gotowym do przekazania 
        do karty dźwiękowej.
    UWAGA: 
      - lewy kanał (kanał o indeksie 0) nie powinien być poddawany modyfikacji!
      - prawy kanał (kanał o indeksie 1) powinien zawierać wynik działania funkcji echo
    
    UWAGA: 
      Wszelkie operacje wykonane na buforze wejściowym w będą widoczne poza 
      funkcją.
      
    '''
    return element