# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.
"""
from idioma import urls, utils
from idioma.base_translator import BaseTranslator
from idioma.models import Detected


class Translator(BaseTranslator):
    def _translate(self, text: str, dest: str, src: str):
        url = urls.TRANSLATE_RPC.format(host=self._pick_service_url())
        data = {
            'f.req': self._build_rpc_request(text, dest, src),
        }
        r = self.client.post(url, params=self.POST_PARAMS, data=data)

        if r.status_code != 200 and self.raise_Exception:
            raise Exception('Unexpected status code "{}" from {}'.format(
                r.status_code, self.service_urls))

        return r.text, r

    def prepare_translate_legacy_params(self, text, src, dest, override):
        token = ''  # dummy default value here as it is not used by api client
        if self.client_type == 'webapp':
            token = self.token_acquirer.do(text)

        params = utils.build_params(client=self.client_type, query=text,
                                    src=src, dest=dest,
                                    token=token, override=override)

        url = urls.TRANSLATE.format(host=self._pick_service_url())
        return url, params

    def _translate_legacy(self, text, dest, src, override):

        url, params = self.prepare_translate_legacy_params(text, src, dest, override)
        response = self.client.get(url, params=params)
        return self.handle_legacy_translate_response(response, text)

    def translate(self, text: str, dest='en', src=None):
        src, dest = self.validate_normalize_src_dest(src, dest)
        data, response = self._translate(text, dest, src)
        return self.parse_response(src, dest, text, data, response)

    def detect(self, text: str):
        translated = self.translate(text, src='auto', dest='en')
        result = Detected(lang=translated.src,
                          confidence=translated.extra_data.get('confidence',
                                                               None),
                          response=translated._response)
        return result

    def detect_legacy(self, text, **kwargs):
        """Detect language of the input text

        :param text: The source text(s) whose language you want to identify.
                     Batch detection is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :rtype: Detected
        :rtype: :class:`list` (when a list is passed)

        Basic usage:
            >>> from idioma import Translator
            >>> translator = Translator()
            >>> translator.detect('이 문장은 한글로 쓰여졌습니다.')
            <Detected lang=ko confidence=0.27041003>
            >>> translator.detect('この文章は日本語で書かれました。')
            <Detected lang=ja confidence=0.64889508>
            >>> translator.detect('This sentence is written in English.')
            <Detected lang=en confidence=0.22348526>
            >>> translator.detect('Tiu frazo estas skribita en Esperanto.')
            <Detected lang=eo confidence=0.10538048>

        Advanced usage:
            >>> langs = translator.detect(['한국어', '日本語', 'English', 'le français'])
            >>> for lang in langs:
            ...    print(lang.lang, lang.confidence)
            ko 1
            ja 0.92929292
            en 0.96954316
            fr 0.043500196
        """
        if isinstance(text, list):
            result = []
            for item in text:
                lang = self.detect(item)
                result.append(lang)
            return result

        data, response = self._translate_legacy(text, 'en', 'auto', kwargs)

        return self.extract_source_language_and_confidence(data, response)
