from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv

from lib import text
from lib.cipher import BookCipher, CaesarCipher, KeyCipher, TranspositionCipher


def parse_args():
    DEFAULT_BOOK_PATH = "material/books/kokoro.txt"

    parser = ArgumentParser(description="暗号化・復号化ツール")
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], required=True, help="暗号化か復号化かを指定")
    parser.add_argument(
        "--cipher", choices=["caesar", "xor", "transposition", "book"], required=True, help="暗号方式 (caesar 暗号, XOR 暗号, 転置 暗号, 書籍 暗号)"
    )
    parser.add_argument("--text", type=str, required=True, help="処理対象の文字列")
    parser.add_argument("--key", type=str, required=False, help="暗号で使う鍵（必要に応じて）")
    parser.add_argument(
        "--book_path", type=Path, default=Path(DEFAULT_BOOK_PATH), help="書籍暗号で使用するテキストファイル（デフォルト: 夏目漱石『こころ』）"
    )
    return parser.parse_args()


def main():
    match args.cipher:
        case "caesar":
            if not args.key or not args.key.isdigit():
                print("❌ Caesar暗号には数値のkeyが必要です")
                return
            cipher = CaesarCipher(int(args.key))
        case "xor":
            if not args.key:
                print("❌ XOR暗号には文字列のkeyが必要です")
                return
            cipher = KeyCipher(args.key)
        case "transposition":
            if not args.key or not args.key.isdigit():
                print("❌ 転置暗号には数値のkeyが必要です")
                return
            cipher = TranspositionCipher(int(args.key))
        case "book":
            if not args.book_path.exists():
                print(f"❌ エラー: 書籍ファイルが見つかりません: {args.book_path}")
                return
            book_lines = text.read_text_file(args.book_path)
            cipher = BookCipher(book_lines)

    match args.mode:
        case "encrypt":
            result = cipher.encrypt(args.text)
        case "decrypt":
            result = cipher.decrypt(args.text)

    print(f"🔐 結果: {result}")


if __name__ == "__main__":
    load_dotenv()
    args = parse_args()
    main()
