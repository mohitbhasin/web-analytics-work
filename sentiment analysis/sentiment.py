"""
Reads a list of reviews and decide if each review is positive or negative,
based on the occurences of positive and negative words.
Writes the results in a file.
"""

POS_FILE, NEG_FILE = 'positive-words.txt', 'negative-words.txt'

def loadLexicon(wordFile):
    """Returns a set of words from a file"""
    return set(line.strip() for line in open(wordFile))

# Let's load the default lexicons at the time of module loading itself
POS_LEX, NEG_LEX = loadLexicon(POS_FILE), loadLexicon(NEG_FILE)

def get_sentiment(line, posLex=POS_LEX, negLex=NEG_LEX):
    """Gets sentiment for a line based on the lexicons.
    returns line, sentiment, positive_words, and negative_words
    """
    words = set(line.split(' '))
    posList = words & posLex # set intersection
    negList = words & negLex 
    diff = len(posList) - len(negList) 
    sentiment = 'Neutral' if diff == 0 else 'Positive' if diff > 0 else 'Negative'
    return (sentiment, posList, negList)

def process_reviews(review_file='nokia.txt', outfile='results.txt', 
                    posLex=POS_LEX, negLex=NEG_LEX):
    """Processes the reviews based on lexicons; we can pass custom lexicons too"""
    lines = ( line.strip() for line in open(review_file) )
    outFmt = '{}\n{}\n{}\n{}\n\n' # line\nPosList\nNegList\nSenti\n\n
    with open('results.txt', 'w') as outfile:
        for line in lines:
            senti, pws, negws = get_sentiment(line, posLex, negLex)
            outfile.write(outFmt.format(line, list(pws), list(negws), senti)) 

def main(review_file='nokia.txt', outfile='results.txt', posFile=None, negFile=None):
    """Processes reviews with optional lexicons for positive and negative reviews"""
    posLex = POS_LEX if not posFile else loadLexicon(posFile)
    negLex = NEG_LEX if not negFile else loadLexicon(negFile)
    process_reviews(review_file, outfile, posLex, negLex)

def print_sentiment(line, **kwargs):
    # you can pass options such as posLex=loadLexicon('new_pos_file') here
    res = get_sentiment(line, **kwargs) 
    fmt = 'Sentiment:{0}; Positive_words:[{1}]; Negative_words:[{2}]; Given_line:[{3}]'
    print(fmt.format(res[0], ','.join(res[1]), ','.join(res[2]), line))
    
def run_tests():
    # Let's randomly sample a set of 20 words from the lexicons
    import random
    Nsample = 20
    pos_words = random.sample(POS_LEX, Nsample)
    neg_words = random.sample(NEG_LEX, Nsample)    
    # careful printing out "negative" words in the NEG_LEX into a notebook
    # there are a lot of "curse words" in there that may make things awkward

    for j in range(Nsample):
        assert get_sentiment(pos_words[j])[0] == 'Positive'
        assert get_sentiment(neg_words[j])[0] == 'Negative'
        ## The next one 'sometimes fails' because we have an overlap of the words
        assert get_sentiment(pos_words[j] + ' ' + neg_words[j])[0] == 'Neutral'

    # assert POS_LEX & NEG_LEX is None
    # This fails because we have a set of overlaps...
    
    '''assert get_sentiment('good nice') == 'Positive'
    assert get_sentiment('worthless') == 'Negative'
    assert get_sentiment('abcdefghijklmnop') == 'Neutral'
    assert get_sentiment('') == 'Neutral'
    assert get_sentiment('good ' * 100) == 'Positive'
    assert get_sentiment('bad ' * 100) == 'Negative' '''
    
if __name__ == "__main__": 
    import sys 
    if len(sys.argv) == 2 and sys.argv[1] == "--test":  # valid if we run as python prog.py --test
        run_tests()
    elif len(sys.argv) == 1: # no arguments were passed
        main()
    else:
        get_sentiment(' '.join(sys.argv[1:]))
        # This is helpful to test one sentence at a time on command-line
