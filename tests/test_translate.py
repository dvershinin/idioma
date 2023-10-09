from idioma import Translator


def test_translate_thai_hello():
    translator = Translator()
    assert translator.translate('안녕하세요').text == 'hello'
