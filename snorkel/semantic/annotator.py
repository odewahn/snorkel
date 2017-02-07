import re

class Annotator:
    """A base class for annotators."""
    def annotate(self, tokens):
        """Returns a list of pairs, each a category and a semantic representation."""
        return []

class TokenAnnotator(Annotator):
    def annotate(self, tokens):
        if len(tokens) == 1:
            return [('$Token', tokens[0]['word'])]
        else:
            return []

class PunctuationAnnotator(Annotator):
    def annotate(self, tokens):
        if len(tokens) == 1:
            if tokens[0]['pos'] == "``":
                return [('$OpenQuote', tokens[0]['word'])]
            elif tokens[0]['pos'] == "\'\'":
                return [('$CloseQuote', tokens[0]['word'])]
            elif tokens[0]['pos'] == "-LRB-":
                return [('$OpenParen', tokens[0]['word'])]
            elif tokens[0]['pos'] == "-RRB-":
                return [('$CloseParen', tokens[0]['word'])]
        return []

class IntegerAnnotator(Annotator):
    def annotate(self, tokens):
        if len(tokens) == 1:
            if all(token['ner'] in ['NUMBER','ORDINAL'] for token in tokens):
                ner_number = tokens[0]['normalizedNER']
                number = re.sub('[^\d\.]','', ner_number)
                value = int(float(number))
                return [('$Int', ('.int', value))]
        return []