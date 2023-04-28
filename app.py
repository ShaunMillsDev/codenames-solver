from gensim.models import KeyedVectors

def get_winner(words, word_limit, MAX_LIMIT):

    if word_limit < MAX_LIMIT:
        model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True, limit=50000)
        
        # set word_list to length of number of words we are using (3 for example)
        word_lists = [[] for _ in range(len(words))]

        # for each word we are using, get the list of similar_words ('word', value)
        for index, word in enumerate(words):
            try:
                similar_word_list = model.most_similar(word, topn=word_limit)
            except Exception as e:
                print(f"An error occured: {e}")
                return []

            # for each similar_word in similar_word_list, take only the word, not the value, and add it to word_list at the index of the word we are using
            for similar_word in similar_word_list:
                word_lists[index].append(similar_word[0])


        # create dictionary to store all words in the first word list that are found in all other word lists (words that are associated to all input words) 
        successful_items = {}

        # set the current word list to the first list in word_lists so that we can check each of it's words against the other word lists' words 
        current_word_list = word_lists[0]
            
        # loop through each item in current_word_list
        for _, item in enumerate(current_word_list):
            item_penalty = 0
            add_item = True

            # loop through each other word_list in word_lists to see if it contains current_item
            # if all the other word lists contains the current_item, total all their indexes and store as current_item_penalty and add to dictionary with key as current_item
            for i in range(1, len(word_lists)):
                word_found_in_current_list = False 
                next_word_list = word_lists[i] # set next_word_list to the next word list in word_lists

                # search for the current word in the next list
                for current_word_index, current_word in enumerate(next_word_list):
                    if (current_word == item):
                        word_found_in_current_list = True
                        item_penalty += current_word_index

                # if the current word hasn't been found in the next list, change add_item to False to indiciate, this word shouldn't be used
                if word_found_in_current_list == False:
                    add_item = False
                    break
                    
            # if the item is to be used, store in successful_items dictionary with item_penalty score
            if (add_item):
                successful_items[item] = item_penalty

        
        # print all successful words that are found all in all lists with their associated penalty (lower is better) sorted by lowest first
        keys_sorted_by_value = sorted(successful_items, key=successful_items.get)

        if len(successful_items) != 0:
            for key in keys_sorted_by_value:
                    print(f"{key}: {successful_items[key]}")
        else:
            word_limit += 25
            print(f"No associations found for the first: {word_limit} associations. Increasing word limit to: {word_limit}")
            get_winner(words, word_limit, MAX_LIMIT)


get_winner(['car', 'pizza', 'tissue'], 900, 1000)