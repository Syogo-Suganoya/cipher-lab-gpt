import sys
from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv

from lib import gemini_api, text, validation
from lib.cipher import BookCipher, CaesarCipher, KeyCipher, TranspositionCipher


def is_meaningful_by_gpt(decrypt_text):
    """
    GPTを使用して、与えられた復号文が意味のある日本語かどうかを判定します。
    """
    if not decrypt_text:
        return False

    prompt = "あなたは文章の自然さを判定するAIです。\n"
    prompt += "以下の文は自然で意味が通じる日本語ですか？端的に「はい」か「いいえ」で答えてください。\n"
    prompt += decrypt_text
    res = gemini_api.query(prompt)
    print(decrypt_text)
    if not res:
        return False
    return res.startswith("はい")


def is_valid_decryption_brute_force(cipher_cls, ciphertext, max_candidates):
    """
    総当たりで意味のある復号文を探す。
    """
    results = []
    candidates = cipher_cls.brute_force(ciphertext)
    for key, decrypted in candidates:
        if is_meaningful_by_gpt(decrypted):
            results.append((f"{cipher_cls.__name__}（key={key}）", decrypted))
            if max_candidates != -1 and len(results) >= max_candidates:
                break
    return results


def is_valid_decryption_single(cipher_instance):
    """
    単一の鍵を使う暗号クラス用
    """
    decrypted = cipher_instance.decrypt(args.encrypt_text)
    if is_meaningful_by_gpt(decrypted):
        return [(cipher_instance.name, decrypted)]
    return []


def main():
    if not args.book_path.exists():
        print(f"❌ エラー: 書籍ファイルが見つかりません: {args.book_path}")
        return

    try:
        validation.validate_greater_equal(args.max_candidates, 0)
    except ValueError as e:
        print(e)
        return

    results = []

    # Caesar（総当たり）
    results += is_valid_decryption_brute_force(CaesarCipher, args.encrypt_text, args.max_candidates)

    # 転置（総当たり）
    results += is_valid_decryption_brute_force(TranspositionCipher, args.encrypt_text, args.max_candidates)

    # XOR（固定キー）
    xor_cipher = KeyCipher(args.key)
    results += is_valid_decryption_single(xor_cipher)

    # 書籍暗号
    book_lines = text.read_text_file(args.book_path)
    book_cipher = BookCipher(book_lines)
    results += is_valid_decryption_single(book_cipher)

    for method, result in results:
        print(f"[✅ {method} 暗号] → {result}")


def parse_args():
    DEFAULT_BOOK_PATH = "material/books/kokoro.txt"

    class CustomArgumentParser(ArgumentParser):
        def error(self, message):
            error_patterns = {
                "the following arguments are required: encrypt_text": "❌ エラー: 暗号文は必須です。",
                "argument --max_candidates: invalid int value:": "❌ エラー: --max_candidates は整数で入力してください。",
            }

            for pattern, error_msg in error_patterns.items():
                if pattern in message:
                    print(f"\n{error_msg}")
                    sys.exit(2)

            # 該当しない場合はデフォルトの処理
            super().error(message)

    parser = CustomArgumentParser(description="暗号解読ツール")
    parser.add_argument("encrypt_text", type=str, help="暗号文")
    parser.add_argument("--key", type=str, default="abc123", help="XOR暗号に使う鍵文字列（デフォルト: abc123）")
    parser.add_argument(
        "--book_path", type=Path, default=Path(DEFAULT_BOOK_PATH), help="書籍暗号で使用するテキストファイル（デフォルト: 夏目漱石『こころ』）"
    )
    parser.add_argument("--max_candidates", type=int, default=0, help="総当たりで意味のある復号を試す最大件数（0で無制限、デフォルト: 0）")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    load_dotenv()
    args = parse_args()
    main()
