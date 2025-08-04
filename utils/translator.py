import re
import asyncio
from googletrans import Translator, LANGCODES

pattern = r'\$translation:([a-z\-]+)'


def translate(full_body, post_content):
    def replace_match(match):
        lang_code = match.group(1)
        if lang_code in LANGCODES.values():
            # Create a new translator instance for each translation to avoid conflicts
            try:
                translator = Translator()
                # Run the async translation in a synchronous context
                translation = asyncio.run(translator.translate(post_content, dest=lang_code))
                return translation.text.replace('\n', '\\n')
            except Exception as e:
                print(f"Translation failed: {e}")
                print(
                    f"Original text: {post_content}, language code: {lang_code}")
                return "<translation failed>"
        return match.group(0)

    return re.sub(pattern, replace_match, full_body)


if __name__ == "__main__":
    sample_full_body = "Here is some text. $translation:zh-cn"
    sample_post_content = "Hello, how are you?"
    result = translate(sample_full_body, sample_post_content)
    print(result)
