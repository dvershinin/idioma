from idioma import Translator


def test_translate_thai_hello():
    translator = Translator()
    assert translator.translate('안녕하세요').text == 'hello'


def test_translate_thai_hello_src_none_auto():
    translator = Translator()
    assert translator.translate('안녕하세요', src=None).text == 'hello'


def test_translate_thai_lang_detect():
    translator = Translator()
    assert translator.detect('안녕하세요').lang == 'ko'
