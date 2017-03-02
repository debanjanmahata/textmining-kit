'''
Created on Mar 1, 2017

@author: debanjan
'''
# -*- coding: utf-8 -*-
"""
Collection of regular expressions and other (small, generally useful) constants.
Source: textacy (https://github.com/chartbeat-labs/textacy)
Also added some of my own
"""
import re
import string

NUMERIC_NE_TYPES = {'ORDINAL', 'CARDINAL', 'MONEY', 'QUANTITY', 'PERCENT', 'TIME', 'DATE'}
SUBJ_DEPS = {'agent', 'csubj', 'csubjpass', 'expl', 'nsubj', 'nsubjpass'}
OBJ_DEPS = {'attr', 'dobj', 'dative', 'oprd'}
AUX_DEPS = {'aux', 'auxpass', 'neg'}

REPORTING_VERBS = {'according', 'accuse', 'acknowledge', 'add', 'admit', 'agree',
                   'allege', 'announce', 'argue', 'ask', 'assert', 'believe', 'blame',
                   'charge', 'cite', 'claim', 'complain', 'concede', 'conclude',
                   'confirm', 'contend', 'criticize', 'declare', 'decline', 'deny',
                   'describe', 'disagree', 'disclose', 'estimate', 'explain', 'fear',
                   'hope', 'insist', 'maintain', 'mention', 'note', 'observe', 'order',
                   'predict', 'promise', 'recall', 'recommend', 'reply', 'report', 'say',
                   'state', 'stress', 'suggest', 'tell', 'testify', 'think', 'urge', 'warn',
                   'worry', 'write'}
#newly added
FUNCTIONAL_WORDS = {'be able to', 'can', 'could', 'dare', 'had better', 'have to', 'may', 'might',
                    'must', 'need to', 'ought', 'ought to', 'shall', 'should', 'used to', 'will',
                    'would', 'accordingly', 'after', 'albeit', 'although', 'and', 'as', 'because',
                    'before', 'both', 'but', 'consequently', 'either', 'for', 'hence', 'however',
                    'if', 'neither', 'nevertheless', 'nor', 'once', 'or', 'since', 'so', 'than',
                    'that', 'then', 'thence', 'therefore', 'tho', 'though', 'thus', 'till', 'unless',
                    'until', 'when', 'whence', 'whenever', 'where', 'whereas', 'wherever', 'whether',
                    'while', 'whilst', 'yet', 'a', 'all', 'an', 'another', 'any', 'both', 'each',
                    'either', 'every', 'her', 'his', 'its', 'my', 'neither', 'no', 'other', 'our',
                    'per', 'some', 'that', 'the', 'their', 'these', 'this', 'those', 'whatever',
                    'whichever', 'your', 'aboard', 'about', 'above', 'absent', 'according to',
                    'across', 'after', 'against', 'ahead', 'ahead of', 'all over', 'along', 'alongside',
                    'amid', 'amidst', 'among', 'amongst', 'anti', 'around', 'as', 'as of', 'as to',
                    'aside', 'astraddle', 'astride', 'at', 'away from', 'bar', 'barring', 'because of',
                    'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'beyond',
                    'but', 'by', 'by the time of', 'circa', 'close by', 'close to', 'concerning',
                    'considering', 'despite', 'down', 'due to', 'during', 'except', 'except for',
                    'excepting', 'excluding', 'failing', 'following', 'for', 'for all', 'from',
                    'given', 'in', 'in between', 'in front of', 'in keeping with', 'in place of',
                    'in spite of', 'in view of', 'including', 'inside', 'instead of', 'into',
                    'less', 'like', 'minus', 'near', 'near to', 'next to', 'notwithstanding',
                    'of', 'off', 'on', 'on top of', 'onto', 'opposite', 'other than', 'out',
                    'out of', 'outside', 'over', 'past', 'pending', 'per', 'pertaining to', 'plus',
                    'regarding', 'respecting', 'round', 'save', 'saving', 'similar to', 'since', 'than',
                    'thanks to', 'through', 'throughout', 'thru', 'till', 'to', 'toward', 'towards',
                    'under', 'underneath', 'unlike', 'until', 'unto', 'up', 'up to', 'upon', 'versus',
                    'via', 'wanting', 'with', 'within', 'without', 'all', 'another', 'any', 'anybody',
                    'anyone', 'anything', 'both', 'each', 'each other', 'either', 'everybody', 'everyone',
                    'everything', 'few', 'he', 'her', 'hers', 'herself', 'him', 'himself', 'his', 'I',
                    'it', 'its', 'itself', 'many', 'me', 'mine', 'myself', 'neither', 'no_one', 'nobody',
                    'none', 'nothing', 'one', 'one another', 'other', 'ours', 'ourselves', 'several',
                    'she', 'some', 'somebody', 'someone', 'something', 'such', 'that', 'theirs', 'them',
                    'themselves', 'these', 'they', 'this', 'those', 'us', 'we', 'what', 'whatever', 'which',
                    'whichever', 'who', 'whoever', 'whom', 'whomever', 'whose', 'you', 'yours', 'yourself',
                    'yourselves', 'a bit of', 'a couple of', 'a few', 'a good deal of', 'a good many',
                    'a great deal of', 'a great many', 'a lack of', 'a little', 'a little bit of',
                    'a majority of', 'a minority of', 'a number of', 'a plethora of', 'a quantity of',
                    'all', 'an amount of', 'another', 'any', 'both', 'certain', 'each', 'either', 'enough',
                    'few', 'fewer', 'heaps of', 'less', 'little', 'loads', 'lots', 'many', 'masses of',
                    'more', 'most', 'much', 'neither', 'no', 'none', 'numbers of', 'one half', 'one third',
                    'one fourth', 'one quarter', 'one fifth', 'one', 'two', 'three', 'four', 'part',
                    'plenty of', 'quantities of', 'several', 'some', 'the lack of', 'the majority of',
                    'the minority of', 'the number of', 'the plethora of', 'the remainder of', 'the rest of',
                    'the whole', 'tons of', 'various'}

CURRENCIES = {'$': 'USD', 'zł': 'PLN', '£': 'GBP', '¥': 'JPY', '฿': 'THB',
              '₡': 'CRC', '₦': 'NGN', '₩': 'KRW', '₪': 'ILS', '₫': 'VND',
              '€': 'EUR', '₱': 'PHP', '₲': 'PYG', '₴': 'UAH', '₹': 'INR'}

POS_REGEX_PATTERNS = {
    'en': {'NP': r'<DET>? <NUM>* (<ADJ> <PUNCT>? <CONJ>?)* (<NOUN>|<PROPN> <PART>?)+',
           'PP': r'<ADP> <DET>? <NUM>* (<ADJ> <PUNCT>? <CONJ>?)* (<NOUN> <PART>?)+',
           'VP': r'<AUX>* <ADV>* <VERB>'}
    }

ACRONYM_REGEX = re.compile(r"(?:^|(?<=\W))(?:(?:(?:(?:[A-Z]\.?)+[a-z0-9&/-]?)+(?:[A-Z][s.]?|[0-9]s?))|(?:[0-9](?:\-?[A-Z])+))(?:$|(?=\W))", flags=re.UNICODE)
EMAIL_REGEX = re.compile(r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}(?:$|(?=\b))", flags=re.IGNORECASE | re.UNICODE)
PHONE_REGEX = re.compile(r'(?:^|(?<=[^\w)]))(\+?1[ .-]?)?(\(?\d{3}\)?[ .-]?)?\d{3}[ .-]?\d{4}(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W))')
NUMBERS_REGEX = re.compile(r'(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))')
PUNCT_REGEX = re.compile('[{0}]+'.format(re.escape(string.punctuation)))
CURRENCY_REGEX = re.compile('[{0}]+'.format(''.join(CURRENCIES.keys())))
LINEBREAK_REGEX = re.compile(r'((\r\n)|[\n\v])+')
NONBREAKING_SPACE_REGEX = re.compile(r'(?!\n)\s+')
URL_REGEX = re.compile(
    r"(?:^|(?<![\w/.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?://|ftp://|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"(?:$|(?![\w?!+&/]))",
    flags=re.UNICODE | re.IGNORECASE)  # source: https://gist.github.com/dperini/729294
SHORT_URL_REGEX = re.compile(
    r"(?:^|(?<![\w/.]))"
    # optional scheme
    r"(?:(?:https?://)?)"
    # domain
    r"(?:\w-?)*?\w+(?:\.[a-z]{2,12}){1,3}"
    r"/"
    # hash
    r"[^\s.,?!'\"|+]{2,12}"
    r"(?:$|(?![\w?!+&/]))",
    flags=re.IGNORECASE)

# regexes for cleaning up crufty terms
DANGLING_PARENS_TERM_RE = re.compile(
    r'(?:\s|^)(\()\s{1,2}(.*?)\s{1,2}(\))(?:\s|$)', flags=re.UNICODE)
LEAD_TAIL_CRUFT_TERM_RE = re.compile(
    r'^([^\w(-] ?)+|([^\w).!?] ?)+$', flags=re.UNICODE)
LEAD_HYPHEN_TERM_RE = re.compile(
    r'^-([^\W\d_])', flags=re.UNICODE)
NEG_DIGIT_TERM_RE = re.compile(
    r'(-) (\d)', flags=re.UNICODE)
WEIRD_HYPHEN_SPACE_TERM_RE = re.compile(
    r'(?<=[^\W\d]) (-[^\W\d])', flags=re.UNICODE)
WEIRD_APOSTR_SPACE_TERM_RE = re.compile(
    r"([^\W\d]+) ('[a-z]{1,2}\b)", flags=re.UNICODE)

