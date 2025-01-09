'''

https://www.codingame.com/training/easy/markov-text-generation

'''


import sys


def debug(message):
    print(message, file=sys.stderr, flush=True)


seed = 0
def pick_option_index(options):
    global seed
    seed += 7
    return seed % options


# Read meta
words = input().split()
depth = int(input())
length = int(input())
seed_text = input()

# Build the dictionary
ngrams = {}
for i in range(len(words) - depth):
    ngram = " ".join([words[i + j] for j in range(depth)])
    
    if not ngram in ngrams:
        ngrams[ngram] = []

    word = words[i + depth]
    if word not in ngrams[ngram]:
        ngrams[ngram].append(word)

debug(ngrams)

phrase = seed_text.split()
while True:
    seed_text = " ".join(phrase[-1*depth:])
    next_words = ngrams[seed_text]
    random_index = pick_option_index(len(next_words))
    next_word = next_words[random_index]
    phrase.append(next_word)

    if len(phrase) == length:
        print(" ".join(phrase))
        break
