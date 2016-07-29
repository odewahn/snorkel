from .meta import SnorkelBase, snorkel_postgres
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import PickleType

class Context(SnorkelBase):
    """A piece of content."""
    __tablename__ = 'context'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'context',
        'polymorphic_on': type
    }


class Corpus(Context):
    """
    A Corpus holds a set of Documents.

    Default iterator is over (Document, Sentence) tuples.
    """
    __tablename__ = 'corpus'
    id = Column(Integer, ForeignKey('context.id'), nullable=False)
    name = Column(String, primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'corpus',
    }

    def __repr__(self):
        return "Corpus (" + str(self.name) + ")"

    def __iter__(self):
        """Default iterator is over (document, document.sentences) tuples"""
        for doc in self.documents:
            yield (doc, doc.sentences)

    def get_sentences(self):
        return [sentence for doc in self.documents for sentence in doc.sentences]


class Document(Context):
    """An object in a Corpus."""
    __tablename__ = 'document'
    id = Column(Integer, ForeignKey('context.id'), nullable=False)
    name = Column(String, primary_key=True)
    corpus_id = Column(Integer, ForeignKey('corpus.id'), primary_key=True)
    corpus = relationship('Corpus', backref=backref('documents', cascade='all, delete-orphan'), foreign_keys=corpus_id)
    file = Column(String)
    attribs = Column(PickleType)

    __mapper_args__ = {
        'polymorphic_identity': 'document',
    }

    def __repr__(self):
        return "Document" + str((self.name, self.corpus))


class Sentence(Context):
    """A sentence Context in a Document."""
    __tablename__ = 'sentence'
    id = Column(Integer, ForeignKey('context.id'))
    document_id = Column(Integer, ForeignKey('document.id'), primary_key=True)
    document = relationship('Document', backref=backref('sentences', cascade='all, delete-orphan'), foreign_keys=document_id)
    position = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    if snorkel_postgres:
        words = Column(postgresql.ARRAY(String), nullable=False)
        char_offsets = Column(postgresql.ARRAY(Integer), nullable=False)
        lemmas = Column(postgresql.ARRAY(String))
        poses = Column(postgresql.ARRAY(String))
        dep_parents = Column(postgresql.ARRAY(Integer))
        dep_labels = Column(postgresql.ARRAY(String))
    else:
        words = Column(PickleType, nullable=False)
        char_offsets = Column(PickleType, nullable=False)
        lemmas = Column(PickleType)
        poses = Column(PickleType)
        dep_parents = Column(PickleType)
        dep_labels = Column(PickleType)

    __mapper_args__ = {
        'polymorphic_identity': 'sentence',
    }

    def __repr__(self):
        return "Sentence" + str((self.document, self.position, self.text))


class Table(Context):
    __tablename__ = 'table'
    id = Column(Integer, ForeignKey('context.id'))
    document_id = Column(Integer, ForeignKey('document.id'), primary_key=True)
    document = relationship('Document', backref=backref('tables', cascade='all, delete-orphan'), foreign_keys=document_id)
    position = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'table',
    }

    def __repr__(self):
        return "Table" + str((self.document.name, self.position))


class Cell(Context):
    __tablename__ = 'cell'
    id = Column(Integer, ForeignKey('context.id'))
    document_id = Column(Integer, ForeignKey('document.id'), primary_key=True)
    table_id = Column(Integer, ForeignKey('table.id'), primary_key=True)
    table = relationship('Table', backref=backref('cells', cascade='all, delete-orphan'), foreign_keys=table_id)
    position = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False) ### TEMPORARY UNTIL PHRASES EXIST ###
    row_num = Column(Integer)
    col_num = Column(Integer)
    html_tag = Column(Text)
    if snorkel_postgres:
        html_attrs = Column(postgresql.ARRAY(String))
        html_anc_tags = Column(postgresql.ARRAY(String))
        html_anc_attrs = Column(postgresql.ARRAY(String))
    else:
        html_attrs = Column(PickleType)
        html_anc_tags = Column(PickleType)
        html_anc_attrs = Column(PickleType)

    __mapper_args__ = {
        'polymorphic_identity': 'cell',
    }

    def __repr__(self):
        return "Cell" + str((self.table.document.name, self.table.position, self.position, self.text))


# =======
# id_attrs        = ['id', 'doc_id', 'doc_name']
# lingual_attrs   = ['words', 'lemmas', 'poses', 'dep_parents', 'dep_labels', 'char_offsets', 'text']
# sentence_attrs  = id_attrs + ['sent_id'] + lingual_attrs
# table_attrs     = id_attrs + ['context_id', 'table_id', 'phrases', 'html']
# cell_attrs      = id_attrs + ['context_id', 'table_id', 'cell_id', 'row_num', 'col_num', \
#                   'html_tag', 'html_attrs', 'html_anc_tags', 'html_anc_attrs']
# phrase_attrs    = cell_attrs + ['phrase_id', 'sent_id'] + lingual_attrs


# Document = namedtuple('Document', ['id', 'file', 'text', 'attribs'])
# Table    = namedtuple('Table', table_attrs)
# Sentence = namedtuple('Sentence', sentence_attrs)
# Cell     = namedtuple('Cell', cell_attrs)
# Phrase   = namedtuple('Phrase', phrase_attrs)
# >>>>>>> tables