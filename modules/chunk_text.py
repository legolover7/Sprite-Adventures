def chunk(text: str, max_length: int=0, content_width: int=0, char_width: int=0):
    """Splits a line of text into a list of strings that are at most max_length in size.
    
        If max_length isn't supplied but content_width and char_width are,
        it will calculate max_length as (content_width // char_width - 1).
    """
    if len(text) == 0 or text == " ":
        return [text]
    
    # Calculate maximum length based on params
    if max_length == 0:
        max_length = content_width // char_width - 1

    max_length = int(max_length)

    words = text.split(" ")
    output = [""]

    while len(words) > 0:
        current_word = words[0]
        # This word and the previous string fits
        if len(current_word) + len(output[-1]) < max_length:
            # Join by a space only if this isn't the first word we've added
            space = " " if output[-1] != "" else ""
            output[-1] = output[-1] + space + current_word
            words.pop(0)

        # This word doesn't fit, but is less than max_length
        elif len(current_word) <= max_length:
            try:
                if output[-1][-1] == "\t":
                    output[-1] = output[-1][:-1]
                elif output[-1][-1] != " ":
                    output[-1] = output[-1] + " "
            except IndexError:
                pass
            output.append(current_word)
            words.pop(0)

        # This word doesn't fit and it's longer than max_length
        else:
            try:
                if output[-1][-1] != " ":
                    output[-1] = output[-1] + " "
            except IndexError:
                pass
            output.append(current_word[:max_length] + "\t")
            words[0] = current_word[max_length:]
        
    return output

def split_lines(text):
    """Splits text on newline characts"""

    output = []
    counter = 0
    while counter < len(text):
        if text[counter] == "\n":
            output.append(text[:counter])
            if len(output) > 1:
                output[-1] = output[-1].replace("\r", "")
                output[-1] = "\r" + output[-1]
            text = "\r" + text[counter+1:]
            counter = 0
        else:
            counter += 1

    output.append(text)
    if len(output) > 1:
        output[-1] = output[-1].replace("\r", "")
        output[-1] = "\r" + output[-1]

    return output

string = "I am doing some expiremental tests and I need to know if this works"
