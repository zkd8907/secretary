import re
import asyncio
from googletrans import Translator, LANGCODES

translator = Translator()
pattern = r'\$translation:([a-z\-]+)'


def translate(full_body, post_content):
    def replace_match(match):
        lang_code = match.group(1)
        if lang_code in LANGCODES.values():
            # Call the async function synchronously
            translation = asyncio.run(
                translate_sync(post_content, lang_code))
            return translation.replace('\n', '\\n')
        return match.group(0)

    return re.sub(pattern, replace_match, full_body)


async def translate_sync(text, lang_code):
    """Async function to handle translation."""
    translation = await translator.translate(text, dest=lang_code)
    return translation.text
