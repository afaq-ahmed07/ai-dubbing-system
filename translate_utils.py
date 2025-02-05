from googletrans import Translator, LANGUAGES

translator = Translator()

def get_supported_languages():
    """
    Return a dictionary mapping language codes to language names.
    """
    return LANGUAGES

def translate_text(text, target_lang):
    """
    Translate the given text into the target language.
    :param text: Text to translate.
    :param target_lang: Language code (e.g., 'es' for Spanish).
    :return: Translated text.
    """
    translation = translator.translate(text, dest=target_lang)
    return translation.text
