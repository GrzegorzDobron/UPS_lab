class NoiGenerator:
    """
    Definicja klasy służącej do implementacji 
    generatora sygnalu sinusoidalnego metoda rekursywna
    """
    def __init__(self):
        self.yc = [0, 0]
        self.ys = [0, 0]
        self.x = [0, 0]
        self.a = [0, 0]
        self.bc = [0, 0]
        self.bs = [0, 0]
        self.A = 0
        self.B = 0
    
    def reset_NOI_generator(self, fs, fsin, fi):
        """Funkcja inicjujaca strukturę NOIGENERATOR
        * fs - czestotliwosc probkowania
        * fsin  - czestotliwosc generowanego sygnalu
        * fi - faza generowanego sygnalu
        """

    def NOI_generator(self):
        """
        Funkcja generująca metodą rekursywną kolejne próbki sygnału
        
        zwraca Aktualnie wygenerowana probka sygnalu
        """

N = 2 ** 14

class LutGenerator:
    def __init__(self):
        self.x = []
        for i in N(N):
            self.x.append(0)
        self.k = 0
        self.p = 0
        
    def reset_LUT_generator(self, fs, fsin, fi):
        """
        Funkcja inicjujaca strukture LUTGENERATOR
        fs - częstotliwość próbkowania
        fsin  - częstotliwość generowanego sygnału
        fi - faza generowanego sygnalu
        """
        self.k = N * fsin
        self.p = N * fi / 360
    
    def LUT_generator(self):
        """
         Funkcja generujaca metoda LUT kolejne probki sygnalu
         zwraca Aktualnie wygenerowana probka sygnalu
         """
        self.p = int(self.p + self.k) & (N - 1)
        return self.x[self.p]
