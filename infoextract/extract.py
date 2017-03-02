'''
Created on Mar 1, 2017

@author: debanjan
'''
from spacy.parts_of_speech import DET
from utils.constants import NUMERIC_NE_TYPES


def words(doc,
          filter_stops=True,
          filter_punct=True,
          filter_nums=False,
          include_pos=None,
          exclude_pos=None):
    """
    Extract an ordered sequence of words from a document processed by spaCy,
    optionally filtering words by part-of-speech tag and frequency.

    Args:
        doc (``spacy.Doc``)
        filter_stops (bool): if True, remove stop words from word list
        filter_punct (bool): if True, remove punctuation from word list
        filter_nums (bool): if True, remove number-like words (e.g. 10, 'ten')
            from word list
        include_pos (str or Set[str]): remove words whose part-of-speech tag
            IS NOT included in this param
        exclude_pos (str or Set[str]): remove words whose part-of-speech tag
            IS in the specified tags

    Yields:
        ``spacy.Token``: the next token from ``doc`` passing specified filters
            in order of appearance in the document

    Raises:
        TypeError: if `include_pos` or `exclude_pos` is not a str, a set of str,
            or a falsy value

    .. note:: Filtering by part-of-speech tag uses the universal POS tag set,
        http://universaldependencies.org/u/pos/
    """
    words_ = (w for w in doc if not w.is_space)
    if filter_stops is True:
        words_ = (w for w in words_ if not w.is_stop)
    if filter_punct is True:
        words_ = (w for w in words_ if not w.is_punct)
    if filter_nums is True:
        words_ = (w for w in words_ if not w.like_num)
    if include_pos:
        if isinstance(include_pos, str):
            include_pos = include_pos.upper()
            words_ = (w for w in words_ if w.pos_ == include_pos)
        elif isinstance(include_pos, (set, frozenset, list, tuple)):
            include_pos = {pos.upper() for pos in include_pos}
            words_ = (w for w in words_ if w.pos_ in include_pos)
        else:
            msg = 'invalid `include_pos` type: "{}"'.format(type(include_pos))
            raise TypeError(msg)
    if exclude_pos:
        if isinstance(exclude_pos, str):
            exclude_pos = exclude_pos.upper()
            words_ = (w for w in words_ if w.pos_ != exclude_pos)
        elif isinstance(exclude_pos, (set, frozenset, list, tuple)):
            exclude_pos = {pos.upper() for pos in exclude_pos}
            words_ = (w for w in words_ if w.pos_ not in exclude_pos)
        else:
            msg = 'invalid `exclude_pos` type: "{}"'.format(type(exclude_pos))
            raise TypeError(msg)

    for word in words_:
        yield word


def ngrams(doc,
           n,
           filter_stops=True,
           filter_punct=True,
           filter_nums=False,
           include_pos=None,
           exclude_pos=None):
    """
    Extract an ordered sequence of n-grams (``n`` consecutive words) from a
    spacy-parsed doc, optionally filtering n-grams by the types and
    parts-of-speech of the constituent words.

    Args:
        doc (``spacy.Doc``)
        n (int): number of tokens per n-gram; 2 => bigrams, 3 => trigrams, etc.
        filter_stops (bool): if True, remove ngrams that start or end
            with a stop word
        filter_punct (bool): if True, remove ngrams that contain
            any punctuation-only tokens
        filter_nums (bool): if True, remove ngrams that contain
            any numbers or number-like tokens (e.g. 10, 'ten')
        include_pos (str or Set[str]): remove ngrams if any of their constituent
            tokens' part-of-speech tags ARE NOT included in this param
        exclude_pos (str or Set[str]): remove ngrams if any of their constituent
            tokens' part-of-speech tags ARE included in this param

    Yields:
        ``spacy.Span``: the next ngram from ``doc`` passing all specified
            filters, in order of appearance in the document

    Raises:
        ValueError: if ``n`` < 1
        TypeError: if `include_pos` or `exclude_pos` is not a str, a set of str,
            or a falsy value

    .. note:: Filtering by part-of-speech tag uses the universal POS tag set,
        http://universaldependencies.org/u/pos/
    """
    if n < 1:
        raise ValueError('n must be greater than or equal to 1')

    ngrams_ = (doc[i: i + n]
               for i in range(len(doc) - n + 1))
    ngrams_ = (ngram for ngram in ngrams_
               if not any(w.is_space for w in ngram))
    if filter_stops is True:
        ngrams_ = (ngram for ngram in ngrams_
                   if not ngram[0].is_stop and not ngram[-1].is_stop)
    if filter_punct is True:
        ngrams_ = (ngram for ngram in ngrams_
                   if not any(w.is_punct for w in ngram))
    if filter_nums is True:
        ngrams_ = (ngram for ngram in ngrams_
                   if not any(w.like_num for w in ngram))
    if include_pos:
        if isinstance(include_pos, str):
            include_pos = include_pos.upper()
            ngrams_ = (ngram for ngram in ngrams_
                       if all(w.pos_ == include_pos for w in ngram))
        elif isinstance(include_pos, (set, frozenset, list, tuple)):
            include_pos = {pos.upper() for pos in include_pos}
            ngrams_ = (ngram for ngram in ngrams_
                       if all(w.pos_ in include_pos for w in ngram))
        else:
            msg = 'invalid `include_pos` type: "{}"'.format(type(include_pos))
            raise TypeError(msg)
    if exclude_pos:
        if isinstance(exclude_pos, str):
            exclude_pos = exclude_pos.upper()
            ngrams_ = (ngram for ngram in ngrams_
                       if all(w.pos_ != exclude_pos for w in ngram))
        elif isinstance(exclude_pos, (set, frozenset, list, tuple)):
            exclude_pos = {pos.upper() for pos in exclude_pos}
            ngrams_ = (ngram for ngram in ngrams_
                       if all(w.pos_ not in exclude_pos for w in ngram))
        else:
            msg = 'invalid `exclude_pos` type: "{}"'.format(type(exclude_pos))
            raise TypeError(msg)

    for ngram in ngrams_:
        yield ngram


def named_entities(doc,
                   include_types=None,
                   exclude_types=None,
                   drop_determiners=True):
    """
    Extract an ordered sequence of named entities (PERSON, ORG, LOC, etc.) from
    a spacy-parsed doc, optionally filtering by entity types and frequencies.

    Args:
        doc (``spacy.Doc``)
        include_types (str or Set[str]): remove named entities whose type IS NOT
            in this param; if "NUMERIC", all numeric entity types ("DATE",
            "MONEY", "ORDINAL", etc.) are included
        exclude_types (str or Set[str]): remove named entities whose type IS
            in this param; if "NUMERIC", all numeric entity types ("DATE",
            "MONEY", "ORDINAL", etc.) are excluded
        drop_determiners (bool): remove leading determiners (e.g. "the")
            from named entities (e.g. "the United States" => "United States")

    Yields:
        ``spacy.Span``: the next named entity from ``doc`` passing all specified
            filters in order of appearance in the document

    Raise:
        TypeError: if `include_types` or `exclude_types` is not a str, a set of
            str, or a falsy value
    """

    nes = doc.ents
    if include_types:
        if isinstance(include_types, str):
            include_types = include_types.upper()
            if include_types == 'NUMERIC':
                include_types = NUMERIC_NE_TYPES  # we now go to next if block
            else:
                nes = (ne for ne in nes if ne.label_ == include_types)
        if isinstance(include_types, (set, frozenset, list, tuple)):
            include_types = {type_.upper() for type_ in include_types}
            nes = (ne for ne in nes if ne.label_ in include_types)
        else:
            msg = 'invalid `include_types` type: "{}"'.format(type(include_types))
            raise TypeError(msg)
    if exclude_types:
        if isinstance(exclude_types, str):
            exclude_types = exclude_types.upper()
            if exclude_types == 'NUMERIC':
                exclude_types = NUMERIC_NE_TYPES  # we now go to next if block
            else:
                nes = (ne for ne in nes if ne.label_ != exclude_types)
        if isinstance(exclude_types, (set, frozenset, list, tuple)):
            exclude_types = {type_.upper() for type_ in exclude_types}
            nes = (ne for ne in nes if ne.label_ not in exclude_types)
        else:
            msg = 'invalid `exclude_types` type: "{}"'.format(type(exclude_types))
            raise TypeError(msg)
    if drop_determiners is True:
        nes = (ne if ne[0].pos != DET else ne[1:] for ne in nes)

    for ne in nes:
        yield ne


def noun_chunks(doc,
                drop_determiners=True):
    """
    Extract an ordered sequence of noun chunks from a spacy-parsed doc, optionally
    filtering by frequency and dropping leading determiners.

    Args:
        doc (``spacy.Doc``)
        drop_determiners (bool): remove leading determiners (e.g. "the")
            from phrases (e.g. "the quick brown fox" => "quick brown fox")
        min_freq (int): remove chunks that occur in `doc` fewer than
            `min_freq` times

    Yields:
        ``spacy.Span``: the next noun chunk from ``doc`` in order of appearance
             in the document
    """
    ncs = doc.noun_chunks
    if drop_determiners is True:
        ncs = (nc if nc[0].pos != DET else nc[1:]
               for nc in ncs)

    for nc in ncs:
        yield nc


def phrase_chunks(doc,
                  filter_stops=True,
                  filter_punct=True,
                  filter_nums=False,
                  include_pos=None,
                  exclude_pos=None,
                  include_types=None,
                  exclude_types=None):
    for ent in doc.ents:
        ent.merge(ent.root.tag_, ent.text, ent.label_)

    for np in doc.noun_chunks:
        if len(np) > 1:
            if np[0].pos_ != "DET":
                np = np
            else:
                np = np[1:]
        np.merge(np.root.tag_, np.text, np.root.ent_type_)

    phrases_ = (w for w in doc if not w.is_space)
    if filter_stops is True:
        phrases_ = (w for w in phrases_ if not w.is_stop)
    if filter_punct is True:
        phrases_ = (w for w in phrases_ if not w.is_punct)
    if filter_nums is True:
        phrases_ = (w for w in phrases_ if not w.like_num)
    if include_pos:
        if isinstance(include_pos, str):
            include_pos = include_pos.upper()
            phrases_ = (w for w in phrases_ if w.pos_ == include_pos)
        elif isinstance(include_pos, (set, frozenset, list, tuple)):
            include_pos = {pos.upper() for pos in include_pos}
            phrases_ = (w for w in phrases_ if w.pos_ in include_pos)
        else:
            msg = 'invalid `include_pos` type: "{}"'.format(type(include_pos))
            raise TypeError(msg)
    if exclude_pos:
        if isinstance(exclude_pos, str):
            exclude_pos = exclude_pos.upper()
            phrases_ = (w for w in phrases_ if w.pos_ != exclude_pos)
        elif isinstance(exclude_pos, (set, frozenset, list, tuple)):
            exclude_pos = {pos.upper() for pos in exclude_pos}
            phrases_ = (w for w in phrases_ if w.pos_ not in exclude_pos)
        else:
            msg = 'invalid `exclude_pos` type: "{}"'.format(type(exclude_pos))
            raise TypeError(msg)
    if include_types:
        if isinstance(include_types, str):
            include_types = include_types.upper()
            if include_types == 'NUMERIC':
                include_types = NUMERIC_NE_TYPES  # we now go to next if block
            else:

                phrases_ = (ne for ne in phrases_ if ne.ent_type and ne.label_ == include_types)

        if isinstance(include_types, (set, frozenset, list, tuple)):
            include_types = {type_.upper() for type_ in include_types}

            phrases_ = (ne for ne in phrases_ if ne.ent_type and ne.label_ in include_types)

        else:
            msg = 'invalid `include_types` type: "{}"'.format(type(include_types))
            raise TypeError(msg)
    if exclude_types:
        if isinstance(exclude_types, str):
            exclude_types = exclude_types.upper()
            if exclude_types == 'NUMERIC':
                exclude_types = NUMERIC_NE_TYPES  # we now go to next if block
            else:

                phrases_ = (ne for ne in phrases_ if ne.ent_type and ne.label_ != exclude_types)

        if isinstance(exclude_types, (set, frozenset, list, tuple)):
            exclude_types = {type_.upper() for type_ in exclude_types}

            phrases_ = (ne for ne in phrases_ if ne.ent_type and ne.label_ not in exclude_types)

        else:
            msg = 'invalid `exclude_types` type: "{}"'.format(type(exclude_types))
            raise TypeError(msg)

    for phrase in phrases_:
        yield phrase
