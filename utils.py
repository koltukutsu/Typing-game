from random import sample

def wpm_calculator(len_words:int, total_time:float) -> float:
    """[Calculates the typing speed based on words per minute]

    Args:
        len_words (int): [length of the words]
        total_time (float): [total amount of time taken to type all the words]

    Returns:
        float: [ratio of words per minute]
    """
    print("this much second:", total_time)
    one_word_typing = len_words / total_time # it will give me the duration of typing one word
    wpm = 60 * one_word_typing
    
    return wpm

def read_words(file_name:str, limit=100) -> list:
    """[reads the file and keeps the words in the memory]

    Args:
        file_name (str): [the file name]

    Returns:
        list: [word list]
    """
    words = []
    with open(file_name) as txt_file:
        for line in txt_file.readlines():
            for word in line.split():
                words.append(word)    
    
    if not (len(words) < limit):
        words = sample(words, limit)

    return words
