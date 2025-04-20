import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.lib.cipher import BookCipher, CaesarCipher, KeyCipher, TranspositionCipher

# テスト用の共通平文
PLAINTEXT = "猫は泣いている"

# 書籍テキスト（BookCipher用）
BOOK_TEXT = """吾輩は猫である
名前はまだ無い
どこで生れたかとんと見当がつかぬ
何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している"""


@pytest.mark.parametrize("shift", [3, 13, 25])
def test_caesar_cipher(shift):
    cipher = CaesarCipher(shift=shift)
    encrypted = cipher.encrypt(PLAINTEXT)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == PLAINTEXT


@pytest.mark.parametrize("key", [2, 4, 6])
def test_transposition_cipher(key):
    cipher = TranspositionCipher(key=key)
    encrypted = cipher.encrypt(PLAINTEXT)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == PLAINTEXT


@pytest.mark.parametrize("key", ["secret", "KEY123", "パスワード"])
def test_key_cipher(key):
    cipher = KeyCipher(key=key)
    encrypted = cipher.encrypt(PLAINTEXT)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == PLAINTEXT


def test_book_cipher():
    cipher = BookCipher(book_text=BOOK_TEXT)
    encrypted = cipher.encrypt(PLAINTEXT)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == " ".join(list(PLAINTEXT))
