from lib.assertions import Assertions
class TestPhraseLength:

    def test_phrase_length(self):
        phrase = input("Enter a phrase: ")
        Assertions.assert_phrase_is_less_than_15_symbols(phrase, "Phrase is more than 15 symbols")