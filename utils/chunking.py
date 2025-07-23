# This function helps us break up long text into smaller, manageable pieces.
# It's like slicing a big loaf of bread into snack-sized portions for the AI to digest!
def chunk_text(text, chunk_size=500):
    """
    Splits the input text into chunks of a specified size (in words).
    This makes it easier for downstream processing and avoids overwhelming the model.
    """
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
