import json
import string
from abc import ABC, abstractmethod
from pathlib import Path


class Cipher(ABC):
    """
    暗号基底クラス
    """

    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        pass


class CaesarCipher(Cipher):
    """
    Caesar 暗号
    """

    def __init__(self, shift: int):
        self.charsets = self.load_charsets()
        self.CHARSET = self.charsets["hiragana"] + self.charsets["katakana"] + self.charsets["numbers"] + self.charsets["choon"]
        self.CHARSET += string.ascii_letters
        self.shift = shift % len(self.CHARSET)
        self.name = "Caesar"

    def load_charsets(self):
        with open(Path("material/charsets.json"), "r", encoding="utf-8") as file:
            return json.load(file)

    def encrypt(self, plaintext: str) -> str:
        return "".join(self._shift_char(char, self.shift) for char in plaintext)

    def decrypt(self, ciphertext: str) -> str:
        return "".join(self._shift_char(char, -self.shift) for char in ciphertext)

    def _shift_char(self, char: str, shift: int) -> str:
        if char in self.CHARSET:
            index = self.CHARSET.index(char)
            return self.CHARSET[(index + shift) % len(self.CHARSET)]
        return char  # 文字セット外はそのまま返す

    @classmethod
    def brute_force(cls, ciphertext: str) -> list[tuple[int, str]]:
        """
        総当たりで全てのshift値（0〜CHARSETの長さ-1）を試す
        :param ciphertext: 暗号文
        :return: (shift値, 復号文) のタプルのリスト
        """
        # 一時的にCHARSETを取得するためにshift=0でインスタンス生成
        dummy = cls(0)
        charset_length = len(dummy.CHARSET)

        results = []
        for shift in range(charset_length):
            cipher = cls(shift)
            decrypted = cipher.decrypt(ciphertext)
            results.append((shift, decrypted))
        return results


class TranspositionCipher(Cipher):
    """
    転置 暗号
    """

    def __init__(self, key: int):
        self.key = key  # カラム数
        self.name = "転置"

    def encrypt(self, plaintext: str) -> str:
        ciphertext = [""] * self.key
        for col in range(self.key):
            pointer = col
            while pointer < len(plaintext):
                ciphertext[col] += plaintext[pointer]
                pointer += self.key
        return "".join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        num_cols = self.key
        num_rows = len(ciphertext) // num_cols
        if len(ciphertext) % num_cols:
            num_rows += 1

        num_shaded_boxes = (num_cols * num_rows) - len(ciphertext)

        plaintext = [""] * num_rows
        col = 0
        row = 0
        for symbol in ciphertext:
            plaintext[row] += symbol
            row += 1
            if (row == num_rows) or (row == num_rows - 1 and col >= num_cols - num_shaded_boxes):
                row = 0
                col += 1
        return "".join(plaintext)

    @classmethod
    def brute_force(cls, ciphertext: str, max_key: int = None) -> list[tuple[int, str]]:
        """
        転置暗号に対する総当たり復号
        :param ciphertext: 暗号文
        :param max_key: 最大キー値（指定しない場合は len(ciphertext) - 1）
        :return: (key, 復号文) のリスト
        """
        results = []
        max_key = max_key or (len(ciphertext) - 1)
        for key in range(2, max_key + 1):  # key=1だと暗号化されていないので除外
            try:
                cipher = cls(key)
                decrypted = cipher.decrypt(ciphertext)
                results.append((key, decrypted))
            except Exception:
                # 例外が出た場合もスキップ
                continue
        return results


class KeyCipher(Cipher):
    """
    XOR 暗号
    """

    def __init__(self, key: str):
        self.key = key
        self.name = "XOR"

    def encrypt(self, plaintext: str) -> str:
        return "".join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(plaintext))

    def decrypt(self, ciphertext: str) -> str:
        return self.encrypt(ciphertext)  # XORは対称暗号なので同じ処理


class BookCipher(Cipher):
    """
    書籍 暗号
    """

    def __init__(self, book_text: str):
        self.lines = book_text.splitlines()
        self.name = "書籍"

    def encrypt(self, plaintext: str) -> str:
        positions = []
        for word in list(plaintext):
            found = False
            for line_num, line in enumerate(self.lines):
                pos = line.find(word)
                if pos != -1:
                    # 行番号-開始位置（すべて1-based）
                    positions.append(f"{line_num + 1}-{pos + 1}")
                    found = True
                    break
            if not found:
                positions.append("??-??")
        return " ".join(positions)

    def decrypt(self, ciphertext: str) -> str:
        words = []
        for code in ciphertext.split():
            try:
                line_str, char_str = code.split("-")
                line = self.lines[int(line_str) - 1]
                char_index = int(char_str) - 1
                word = line[char_index : char_index + 1]
                words.append(word)
            except Exception:
                words.append("<?>")
        res = " ".join(words)
        if res == "<?>":
            res = ""
        return res
