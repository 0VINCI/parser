#Paweł Wróblewski 253500
class ArithmeticParser:
    def __init__(self, expression):
        self.expression = expression  # Przechowuje przetwarzane wyrażenie
        self.char = 0  # Bieżąca pozycja w wyrażeniu
        self.length = len(expression)  # Długość wyrażenia

    def next_char(self):
        # Przechodzi do następnego znaku w wyrażeniu
        if self.char < self.length - 1:
            self.char += 1
        else:
            self.char = self.length  # Ustawiamy na koniec, jeśli osiągnęliśmy 'EOF'

    def check_first(self, first_set):
        # Sprawdza, czy bieżący znak znajduje się w podanym zbiorze znaków
        if self.char < self.length:
            return self.expression[self.char] in first_set
        return False

    def read_S(self):
        # Próbuje przeczytać całe wyrażenie i sprawdza, czy kończy się średnikiem
        if self.read_W():
            if self.check_first({';'}):
                self.next_char()
                return self.char == self.length  # Sprawdzamy, czy jesteśmy na końcu
        return False

    def read_W(self):
        # Próbuje przeczytać wyrażenie z operacjami
        if self.read_P():
            while self.check_first({'*', '/', '+', '-', '^'}):
                self.next_char()  # Przesuwamy się do następnego znaku po operatorze
                if not self.read_P():
                    return False
            return True
        return False

    def read_P(self):
        # Próbuje przeczytać nawiasy lub liczby
        if self.check_first({'('}):  # Sprawdzamy, czy wyrażenie zaczyna się od nawiasu
            self.next_char()
            if self.read_W():
                if self.check_first({')'}):
                    self.next_char()
                    return True
            return False
        elif self.read_R():
            return True
        return False

    def read_R(self):
        # Próbuje przeczytać liczby, zarówno całkowite jak i zmiennoprzecinkowe
        dot_encountered = False  # Flaga wskazująca, czy napotkano kropkę
        digit_encountered = False  # Flaga wskazująca, czy napotkano cyfrę

        while True:
            if self.check_first({'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}):
                digit_encountered = True
                self.next_char()
            elif self.check_first({'.'}) and not dot_encountered:
                dot_encountered = True
                self.next_char()
                if not self.check_first({'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}):
                    return False  # Niepoprawne, jeśli kropka nie jest śledzona przez cyfrę
            else:
                break  # Wyjście z pętli, jeśli następny znak nie jest ani cyfrą, ani kropką

        return digit_encountered  # Zwraca True tylko, jeśli napotkano przynajmniej jedną cyfrę


while True:
    expression = input("Proszę wpisać wyrażenie arytmetyczne zakończone średnikiem (;) lub wpisz 'exit' aby wyjść: ")
    if expression.lower() == 'exit':
        break
    parser = ArithmeticParser(expression)
    if parser.read_S():
        print("Wyrażenie jest zgodne z gramatyką.")
    else:
        print("Wyrażenie nie jest zgodne z gramatyką.")
