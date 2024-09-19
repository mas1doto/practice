class Enigma:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self, text, ref, rot1, shift1, rot2, shift2, rot3, shift3, pairs=""):
        self._rotors = [Rotor(rot3, shift3), Rotor(rot2, shift2), Rotor(rot1, shift1)]
        self._reflector = Reflector(ref)
        self._connector = Connector(pairs)
        self._prepared_text = "".join(i for i in text.upper() if i in self.ALPHABET)
        self._encrypted_text = ""

    def caesar(self, text, key, alphabet=ALPHABET):

        return alphabet[(alphabet.index(text) + key) % len(alphabet)]

    def cypher(self, symbol,  reverse=False):
        rotors = reversed(self._rotors) if reverse else self._rotors
        for rotor in rotors:
            symbol = self.caesar(symbol, rotor.shift)
            symbol = rotor.connect(symbol, reverse)
            symbol = self.caesar(symbol, -rotor.shift)
        return symbol

    def encrypt(self):
        encrypted_text = []
        if not self._connector.is_correct():
            self._encrypted_text = "Извините, невозможно произвести коммутацию"
            return

        for symbol in self._prepared_text:
            if symbol in self._connector.pairs:
                symbol = self._connector.pairs[symbol]

            self.rotate_rotors()
            encrypted_symbol = self.cypher(symbol)
            encrypted_symbol = self._reflector.reflect(encrypted_symbol)
            encrypted_symbol = self.cypher(encrypted_symbol, reverse=True)

            if encrypted_symbol in self._connector.pairs:
                encrypted_symbol = self._connector.pairs[encrypted_symbol]

            encrypted_text.append(encrypted_symbol)
        self._encrypted_text = ''.join(encrypted_text)

    def rotate_rotors(self):
        rotor3, rotor2, rotor1 = self._rotors
        rotor3.shift += 1
        if rotor3.rotate_condition() == rotor3.shift:
            rotor2.shift += 1
        if rotor2.right_to_turn:
            rotor2.shift += 1
            rotor1.shift += 1
        rotor2.right_to_turn = rotor2.shift == rotor2.rotate_condition() - 1

    @property
    def encrypted_text(self):
        return self._encrypted_text


class Rotor:
    TURNING_CONDITION = {1: 17, 2: 5, 3: 22, 4: 10, 5: 0}
    ROTORS = {0: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              1: 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
              2: 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
              3: 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
              4: 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
              5: 'VZBRGITYUPSDNHLXAWMJQOFECK',
              6: 'JPGVOUMFYQBENHZRDKASXLICTW',
              7: 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
              8: 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
              'beta': 'LEYJVCNIXWPBQMDRTAKZGFUHOS',
              'gamma': 'FSOKANUERHMBTIYCWLQPZXVGJD'
              }
    ALPHABET_LENGTH = 26

    def __init__(self, name, shift):
        self._name = name
        self._alphabet = self.ROTORS[name]
        self._shift = shift
        self._right_to_turn = False

    def connect(self, symbol, reverse=False):
        in_alph, out_alph = (self.ROTORS[0], self._alphabet) if reverse else (self._alphabet, self.ROTORS[0])
        encrypted_symbol = in_alph[out_alph.index(symbol)]
        return encrypted_symbol

    def rotate_condition(self):
        return self.TURNING_CONDITION[self._name]

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift):
        self._shift = shift % self.ALPHABET_LENGTH

    @property
    def right_to_turn(self):
        return self._right_to_turn

    @right_to_turn.setter
    def right_to_turn(self, right_to_turn):
        self._right_to_turn = right_to_turn


class Reflector:
    REFLECTORS = {0: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                  1: 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
                  2: 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
                  3: 'ENKQAUYWJICOPBLMDXZVFTHRGS',
                  4: 'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
                  }
    def __init__(self, name):
        self._alphabet = self.REFLECTORS[name]

    def reflect(self, symbol):
        start_reflector, end_reflector = self.REFLECTORS[0], self._alphabet
        encrypted_symbol = start_reflector[end_reflector.index(symbol)]
        return encrypted_symbol


class Connector:
    def __init__(self, pairs):
        self._pairs_list = list(pairs.upper().replace(" ", ""))
        self._pairs = self.__make_pairs()

    def is_correct(self):
        return len(self._pairs_list) % 2 == 0 and (len(self._pairs_list) == len(set(self._pairs_list)))

    def __make_pairs(self):
        pairs = dict(zip(self._pairs_list[0::2], self._pairs_list[1::2]))
        revered_pairs = {v: k for k, v in pairs.items()}
        pairs.update(revered_pairs)
        return pairs

    def connect(self, symbol):
        return self._pairs[symbol]

    @property
    def pairs(self):
        return self._pairs

