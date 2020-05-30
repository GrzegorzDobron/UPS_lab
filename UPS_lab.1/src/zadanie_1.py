def NWD(a, b):      #definicja funkcji NWD, ktora pobiera dwie zmienne
    c = 0           #zmienna pomocnicza
    while b != 0:   #warunek, ze b to nie 0
        c = a % b   #przypisanie do c calkowitej reszty z dzielenia a i b
        a, b = b, c #'swap', w wyniku tego: a=b, b=c
    return a        #zwracana wartosc przez fukcje NWD

a = int(input("podaj pierwsza liczba calkowita dodatnia: "))                    #wczytanie wartosci zmiennej a
b = int(input("podaj druga liczbe calkowita dodatnia: "))                       #wczytanie wartosci zmiennej b
print("NWD {a} i {b} jest rowny: {NWD}".format(a = a, b = b, NWD = NWD(a, b)))  #przekazanie a i b do funkcji NWD, wypisanie wartosci zwroconej przez funkcje NWD


