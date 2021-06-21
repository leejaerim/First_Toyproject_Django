import random, string
def get_name():
    # get user input
    # read word lists
    with open('nouns.txt', 'r') as infile:
        nouns = infile.read().strip(' \n').split('\n')
    with open('adjectives.txt', 'r') as infile:
        adjectives = infile.read().strip(' \n').split('\n')
    # generate usernames
    # construct username
    word1 = random.choice(adjectives)
    word2 = random.choice(nouns)
    #else make and print the username
    #captilaize first letter
    word1 =word1.title()
    word2 =word2.title()
    username = '{}{}'.format(word1, word2)
    # success
    print(username)
    return username

