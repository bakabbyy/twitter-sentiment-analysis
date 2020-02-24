import re
import string
from sklearn.feature_extraction.text import CountVectorizer
import pickle


class nlp_preprocessor:

    def __init__(self, vectorizer=CountVectorizer(), tokenizer=None, cleaning_function=None,
                 stemmer=None, model=None):
        """
        A class for pipelining our data in NLP problems. The user provides a series
        of tools, and this class manages all of the training, transforming, and
        modification of the text data.
        ---
        :param vectorizer: The model to use for vectorization of text data.
        :param tokenizer: The tokenizer to use, if None defaults to split on spaces.
        :param cleaning_function: How to clean the data, if None defaults to the
        built in class
        """

        if not tokenizer:
            tokenizer = self.splitter
        if not cleaning_function:
            cleaning_function = self.clean_text
        self.stemmer = stemmer
        self.tokenizer = tokenizer
        self.model = model
        self.cleaning_function = cleaning_function
        self.vectorizer = vectorizer
        self._is_fit = False

    def splitter(self, text):
        """
        Default tokenizer that splits on spaces naively.
        ---
        :param text: Input text.
        :return: Text split into a list by white space.
        """

        return text.split(' ')

    def clean_text(self, text, tokenizer, stemmer):
        """
        A naive function to lowercase all words and clean them quickly. This is
        the default behavior if no other cleaning function is specified.
        ---
        :param text: Input text.
        :param tokenizer: The tokenizer to use, if None defaults to split on spaces.
        :return: List of cleaned text, prepared to be fit to a model.
        """

        cleaned_text = []
        for post in text:
            cleaned_words = []
            for word in tokenizer(post):
                low_word = word.lower()
                no_num = re.sub('/w*/d/w*', ' ', low_word)
                for punctuation in string.punctuation:
                    no_punc = no_num.replace(punctuation, '')
                if stemmer:
                    clean_word = stemmer.stem(no_punc)
                cleaned_words.append(clean_word)
            cleaned_text.append(' '.join(cleaned_words))

        return cleaned_text

    def fit(self, text):
        """
        Cleans the data and then fits the vectorizer with the user provided text.
        ---
        :param text: Input text.
        """

        clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer)
        self.vectorizer.fit(clean_text)
        self._is_fit = True

    def transform(self, text):
        """
        Cleans any provided data ad then transforms the data into a vectorized
        format based on the fit function. Returns the vectorized form of the data.
        ---
        :param text: Input text.
        """

        if not self._is_fit:
            raise ValueError('Must fit the models before transforming.')
        clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer)

        return self.vectorizer.transform(clean_text)

    def save_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file allowing a pipeline to be
        loaded later with the pre-trained pieces in place.
        ---
        :param filename: Name of the pickle file to dump pipe results.
        """

        if type(filename) != str:
            raise TypeError('File name must be a string.')
        pickle.dump(self.__dict__, ope(filename+'.mdl', 'wb'))

    def load_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file allowing a pipeline to be
        loaded later with the pre-trained pieces in place.
        ---
        :param filename: name of the pickle file to load.
        """

        if type(filename) != str:
            raise TypeError('File name must be a stringn.')
        if filename[-4:] != '.mdl':
            filename += '.mdl'
        self.__dict__ = pickle.load(open(filename, 'rb'))