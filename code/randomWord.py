import random

class RandomWord:
    word_list: list[str] = ["apple", "grape", "peach", "berry", "melon", "mango", "lemon", "plum", "kiwi", "cherry"]
    def get_word(self) -> str: # gets a random 5 letter word from a website.
        return random.choice(self.word_list)
