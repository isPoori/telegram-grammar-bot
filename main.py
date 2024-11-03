# Developer : Pouria Hosseini | Telegram : @isPoori | CHANNEL : @OmgaDeveloper #
import difflib
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CallbackContext
from textblob import TextBlob
import uuid

VALID_WORDS = [
    "please", "hello", "world", "example", "telegram", "message", "check", "grammar", "spelling",
]

def find_closest_word(word):
    closest_matches = difflib.get_close_matches(word, VALID_WORDS, n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None

def check_grammar_and_spelling(query: str) -> tuple:
    text_blob = TextBlob(query)
    corrected_text = str(text_blob.correct())
    
    words = query.split()
    suggestions = []
    
    for word in words:
        if str(TextBlob(word).correct()) != word:
            closest_word = find_closest_word(word)
            if closest_word:
                suggestions.append((word, closest_word))
    
    if suggestions:
        return (corrected_text, suggestions)
    else:
        return (None, query) 

def inline_query(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query.strip()

    if not query:
        return
    corrected_text, issues = check_grammar_and_spelling(query)

    if issues:
        response_text = f"مشکلات: {', '.join([f'{word} -> {suggestion}' for word, suggestion in issues])}"
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"مشکلات: {query}",
                input_message_content=InputTextMessageContent(f"مشکلات در: {query}"),
                description=response_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("ارسال متن اصلاح شده", switch_inline_query=corrected_text)]
                ])
            )
        ]
    else:
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="متن شما صحیح است.",
                input_message_content=InputTextMessageContent(query)
            )
        ]

    update.inline_query.answer(results)

def main():
    updater = Updater("Token", use_context=True) #Token
    
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inline_query))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()