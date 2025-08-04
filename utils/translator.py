import re
import asyncio
import concurrent.futures
from googletrans import Translator, LANGCODES

TRANSLATION_PATTERN = r'\$translation:([a-z\-]+)'


def _run_async_translation(source_text, target_language):
    """Run async translation in a new event loop"""
    translator = Translator()
    return asyncio.run(translator.translate(source_text, dest=target_language))


def _translate_text(source_text, target_language):
    """Handle the actual translation with proper async management"""
    try:
        # Try to get existing event loop
        asyncio.get_running_loop()
        # If we're in an async context, create a new thread for the translation
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(_run_async_translation, source_text, target_language)
            translation = future.result()
    except RuntimeError:
        # No running event loop, safe to use asyncio.run directly
        translation = _run_async_translation(source_text, target_language)
    
    return translation.text.replace('\n', '\\n')


def _replace_translation_match(match, source_text):
    """Replace a single translation match with translated text"""
    target_language = match.group(1)
    
    if target_language not in LANGCODES.values():
        return match.group(0)
    
    try:
        return _translate_text(source_text, target_language)
    except Exception as e:
        print(f"Translation failed: {e}")
        print(f"Original text: {source_text}, language code: {target_language}")
        return "<translation failed>"


def translate(template, source_text):
    """Translate text in template using source_text as content to translate"""
    return re.sub(TRANSLATION_PATTERN, lambda match: _replace_translation_match(match, source_text), template)


if __name__ == "__main__":
    # Test sequential calls like in main.py
    print("=== Testing sequential calls (like main.py) ===")
    
    test_cases = [
        ("Message 1: $translation:zh-cn", "Hello, how are you?"),
        ("Message 2: $translation:es", "Good morning everyone!"),
        ("Message 3: $translation:fr", "Thank you very much!"),
    ]
    
    for i, (full_body, post_content) in enumerate(test_cases):
        print(f"\nCalling translate #{i+1}:")
        print(f"  Input: {post_content}")
        result = translate(full_body, post_content)
        print(f"  Result: {result}")
    
    print("\n" + "="*50)
    
    # Also test the original simple case
    sample_full_body = "Here is some text. $translation:zh-cn"
    sample_post_content = "Hello, how are you?"
    result = translate(sample_full_body, sample_post_content)
    print(f"Single test result: {result}")
