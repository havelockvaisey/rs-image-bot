def create_bigram(word, spacer = ''):
    return [word[i]+spacer+word[i+1]for i in range(len(word) - 1)]

def create_trigram(word,spacer=''):
    return [word[i]+spacer+word[i+1]+spacer+word[i+2]for i in range(len(word) - 2)]

def create_ngram(word, n = 2, spacer = ''):
    word2 = []
    word3 = ''
    for i in range(len(word)-n+1):
        for m in range(n):
            word3 = word3 + word[i+m] +spacer#+spacer+word[i+m+1]+spacer
            # word2.append(word[i+m]+spacer+word[i+m+1]+spacer)
            # word2.append(word2+word[i]+word[i+m+1])
        word2.append(word3)
        word3 = ''
    return word2

def create_bigram2(word, spacer = ''):
    word2 = []
    for i in range(len(word) - 1):
        word2.append(word[i]+spacer+word[i+1])
    return word2


def get_similarity_ratio(word1,word2):
    # gives the similarity ratio of two words
    word1, word2 = word1.lower(), word2.lower()

    common = []

    bigram1, bigram2 = create_bigram(word1),create_bigram(word2)

    for i in range(len(bigram1)):
        # check to find a common element
        try:
            common_elmnt = bigram2.index(bigram1[i])
            common.append(bigram1[i])
        except:
            continue

    return len(common)/max(len(bigram1), len(bigram2))

def autoCorrect(word, database, sim_threshold = 0.5):
    max_sim = 0.0
    most_sim_word = word

    for data_word in database:
        cur_sim = get_similarity_ratio(word, data_word)
        # print(data_word + '  ' + str(cur_sim)) shows name and ismilarity
        if cur_sim > max_sim:
            max_sim = cur_sim
            most_sim_word = data_word
    
    return most_sim_word if max_sim>sim_threshold else word

def autoCorrectAndSim(word, database, sim_threshold = 0.5):
    max_sim = 0.0
    most_sim_word = word

    for data_word in database:
        cur_sim = get_similarity_ratio(word, data_word)
        if cur_sim > max_sim:
            max_sim = cur_sim
            most_sim_word = data_word
    
    return most_sim_word, max_sim if max_sim>sim_threshold else word, max_sim

# db1 = open("db1.txt","r")
# for line in db1:
#     fields = line.split("\n")
#     print(fields[0])
# print(db1)
# print(autoCorrect('miging',db1))