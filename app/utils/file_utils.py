import chardet
import codecs

def detect_encoding(file_path):
    """
    Detecta o encoding de um arquivo usando a biblioteca `chardet`.

    Args:
        file_path (str): Caminho completo do arquivo a ser analisado.

    Returns:
        str: O encoding detectado do arquivo.

    Raises:
        IOError: Se o arquivo não puder ser lido.
    """
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']


def fix_csv_encoding(file_path, output_path=None):
    """
    Corrige problemas de encoding em arquivos CSV:
    - Detecta automaticamente o encoding do arquivo de origem.
    - Converte o arquivo para o encoding desejado (padrão: UTF-8).
    - Substitui padrões comuns de caracteres quebrados.

    Args:
        file_path (str): Caminho completo do arquivo CSV original.
        output_path (str, opcional): Caminho onde o arquivo corrigido será salvo.
            Se não for fornecido, sobrescreve o arquivo original.

    Returns:
        None: Salva o arquivo corrigido no caminho especificado.

    Raises:
        Exception: Se ocorrer erro ao ler ou salvar o arquivo.
    """
    if not output_path:
        output_path = file_path

    source_encoding = detect_encoding(file_path)
    print(f"Encoding detectado: {source_encoding}")

    replacements = {
        "Ã§": "ç",
        "Ã£": "ã",
        "Ã¡": "á",
        "Ã©": "é",
        "Ãª": "ê",
        "Ã³": "ó",
        "Ã´": "ô",
        "Ãº": "ú",
        "Ã¼": "ü",
        "Ã ": "à",
        "Ã¢": "â",
        "Ã™": "Ù",
        "Ã–": "Ö",
        "Ã": "Ç",
        "Ã€": "À",
        "ÃŸ": "ß",
        "â€œ": "“",
        "â€": "”",
        "â€˜": "‘",
        "â€™": "’",
        "â€“": "–",
        "â€”": "—",
        "â€": "†",
        "Â": "",
    }

    with codecs.open(file_path, "r", encoding=source_encoding) as file:
        content = file.read()

    for broken_char, correct_char in replacements.items():
        content = content.replace(broken_char, correct_char)
        print(f"Substituindo: {broken_char} -> {correct_char}")

    with codecs.open(output_path, "w", encoding="latin1") as file:
        file.write(content)

    print(f"Arquivo corrigido e salvo em: {output_path}")
