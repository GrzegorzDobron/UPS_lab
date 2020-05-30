BUF = 'c78rc783ncr78nr7c810010cn874378cyct8710010010'  #dane_wejsciowe
BITS_LIMITS = 5                                     #ramka_danych 
MODEL ='10010'                                      #szukana_ramka_danych

def signal_success():
    print("success")
def signal_error():
    print("error")

class HowLongString:                                #klasa_liczaca_dlugosc_BUFa
    def run(self):
        BUF.strip()                                 #usuwanie_spacji_z_BUFa
        if (len(BUF) < BITS_LIMITS):                                                #warunek_dlugosci_BUFa-BUF_krotszy_niz_ramka_MODELu
            print("wczytany string ma", len(BUF), "znaki\nString zakrotki")
            signal_error()
            return exit()
        if (len(BUF)>= BITS_LIMITS):                                                #warunek_dlugosci_BUFa-BUF_dluzszy_lub_rowny_niz_ramka_MODELu
            print("wczytany string ma", len(BUF), "znakow")
            if (len(BUF)%BITS_LIMITS == 0):
                return ChannelStateMachine.rangeselect_string
            else:
                print("ostani pakiet danych niekompletny\n")
                return ChannelStateMachine.rangeselect_string

class RangeSelect_string:                                                            #klasa_szukaja_MODELu_w_BUF
        def run(self):
            print("zdefiniowany ciag znakow:\t", BUF)
            if (MODEL in BUF):
                print("kombinacja",MODEL,"zostala wykryta w ciagu znakow")
                return ChannelStateMachine.rangeselect_division
            else:
                print("kombinacja",MODEL,"nie zostala wykryta w ciagu znakow")
                return exit()

class RangeSelect_division:                                                         #klasa_dzielaca_i_szukaja_MODELu_w_5bitowych_pakietach_BUF
    def run(self):
        DivisionString = [BUF[i:i+BITS_LIMITS] for i in range(0, len(BUF), BITS_LIMITS)]    #podzial_BUFa_na_liste
        print("\npakiety 5-bitowych danych:\t", DivisionString)
        if (MODEL in DivisionString):
            print("kombinacja",MODEL,"zostala wykryta w pakietach 5-bitowych")
            return exit()   
        else:
            print("kombinacja",MODEL,"nie zostala wykryta w pakietach 5-bitowych")
            return exit()                                             

class ChannelStateMachine:
    howlongstring = HowLongString()
    rangeselect_division = RangeSelect_division()
    rangeselect_string = RangeSelect_string()
    
    def __init__(self):
        self.currentState = ChannelStateMachine.howlongstring
        while (1):
            self.currentState = self.currentState.run()