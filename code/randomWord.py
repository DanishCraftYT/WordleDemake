import requests

class RandomWord:
    @staticmethod
    def get_word(): # gets a random 5 letter word from a website.
        return requests.get("https://random-word-api.herokuapp.com/word?length=5").text.replace("[", "").replace("\"", "").replace("]", "")
