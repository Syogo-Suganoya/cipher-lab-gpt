暗号AI解読ツール と 暗号化・復号化ツール を作りました。

---

# Cipher Inspector - 暗号解読ツール

## 概要

Cipher Inspectorは、複数の暗号方式に対応した暗号解読ツールです。総当たり攻撃や固定キーを使用した復号を行い、復号結果が意味のある日本語かどうかをAI（GPT）を活用して判定します。また、書籍暗号のような特殊な暗号方式にも対応しています。

## 主な機能

1. **総当たり攻撃による復号**
   - Caesar暗号や転置暗号に対して総当たりで復号を試みます。

2. **固定キーによる復号**
   - XOR暗号など、固定キーを使用する暗号方式に対応しています。

3. **書籍暗号の復号**
   - 指定された書籍テキストを使用して書籍暗号を解読します。

4. **AIによる意味判定**
   - 復号結果が意味のある日本語かどうかをGPTを使用して判定します。

## 使用技術

- **Pythonライブラリ**
  - `argparse`: コマンドライン引数の処理
  - `dotenv`: 環境変数の管理
  - `pathlib`: ファイルパスの操作
  - 独自ライブラリ（`lib`ディレクトリ内）
    - `gemini_api`: GPTを使用したAPIクエリ
    - `cipher`: 各種暗号アルゴリズムの実装
    - `text`: テキストファイルの読み込み
    - `validation`: 入力値の検証

## 必要な環境

- Python 3.8以上
- 必要なライブラリ（`requirements.txt`に記載）
- GPT APIキー（環境変数で設定）

## インストール

1. 必要なライブラリをインストールします。

    ```bash
    pip install -r requirements.txt
    ```

2. 環境変数を設定します。`.env` ファイルを作成し、以下の内容を記載してください。

    ```env
    GEMINI_API_KEY="YOUR_API_KEY"
    ```

## 実行方法

### 基本的な使い方

以下のコマンドを実行して暗号文を復号します。

```bash
python cipher_inspector.py "暗号文"
```

### オプション

- `--key`: XOR暗号で使用する鍵文字列（デフォルト: `abc123`）
- `--book_path`: 書籍暗号で使用するテキストファイルのパス（デフォルト: 夏目漱石『こころ』）
- `--max_candidates`: 総当たりで試す最大件数（0で無制限、デフォルト: 0）

例：

```bash
python cipher_inspector.py "暗号文" --key "my_secret_key" --max_candidates 10
```

## ファイル構成

- `src/`
  - `cipher_inspector.py`: メインスクリプト
  - `lib/`: 暗号アルゴリズムやユーティリティ関数を格納
- `material/`
  - `books/`: 書籍暗号で使用するテキストファイル
- `.env`: 環境変数ファイル（APIキーを設定）

## 注意事項

- GPTを使用するため、APIキーが必要です。
- 復号結果の判定はAIに依存しており、必ずしも正確であるとは限りません。
- 書籍暗号を使用する場合、指定された書籍ファイルが存在する必要があります。

---

# Cipher Tool - 暗号化・復号化ツール

## 概要

Cipher Toolは、複数の暗号方式に対応した暗号化および復号化を行うツールです。コマンドラインから簡単に暗号化・復号化を実行でき、Caesar暗号、XOR暗号、転置暗号、書籍暗号に対応しています。

## 主な機能

1. **暗号化**
   - 指定された暗号方式を使用してテキストを暗号化します。

2. **復号化**
   - 暗号化されたテキストを指定された方式で復号化します。

3. **書籍暗号対応**
   - 書籍テキストを使用した暗号化・復号化が可能です。

## 使用技術

- **Pythonライブラリ**
  - `argparse`: コマンドライン引数の処理
  - `dotenv`: 環境変数の管理
  - `pathlib`: ファイルパスの操作
  - 独自ライブラリ（`lib`ディレクトリ内）
    - `cipher`: 各種暗号アルゴリズムの実装
    - `text`: テキストファイルの読み込み

## 必要な環境

- Python 3.8以上
- 必要なライブラリ（`requirements.txt`に記載）

## インストール

1. 必要なライブラリをインストールします。

    ```bash
    pip install -r requirements.txt
    ```

2. 環境変数を設定します。`.env` ファイルを作成し、必要な設定を記載してください。

## 実行方法

以下のコマンドを使用して暗号化または復号化を実行します。

```bash
python cipher_tool.py --mode <encrypt|decrypt> --cipher <caesar|xor|transposition|book> --text <文字列> [オプション]
```

### 必須引数

- `--mode`: 実行モードを指定（`encrypt`または`decrypt`）
- `--cipher`: 使用する暗号方式を指定（`caesar`, `xor`, `transposition`, `book`）
- `--text`: 処理対象の文字列を指定

### オプション引数

- `--key`: 暗号で使用する鍵（Caesar暗号、XOR暗号、転置暗号で必要）
- `--book_path`: 書籍暗号で使用するテキストファイルのパス（デフォルト: 夏目漱石『こころ』）

### 使用例

#### Caesar暗号で暗号化

```bash
python cipher_tool.py --mode encrypt --cipher caesar --text "hello" --key 3
```

#### XOR暗号で復号化

```bash
python cipher_tool.py --mode decrypt --cipher xor --text "encrypted_text" --key "my_secret_key"
```

#### 書籍暗号で暗号化

```bash
python cipher_tool.py --mode encrypt --cipher book --text "秘密のメッセージ" --book_path "material/books/kokoro.txt"
```

## ファイル構成

- `src/`
  - `cipher_tool.py`: メインスクリプト
  - `lib/`: 暗号アルゴリズムやユーティリティ関数を格納
- `material/`
  - `books/`: 書籍暗号で使用するテキストファイル
- `.env`: 環境変数ファイル（必要に応じて設定）

## 注意事項

- 書籍暗号を使用する場合、指定された書籍ファイルが存在する必要があります。
- 入力値が正しくない場合、エラーメッセージが表示されます。
