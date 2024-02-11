"""
Description:
    This file contains all the code used to search things in this project.
"""

from fuzzywuzzy import fuzz


# search qna_list
def qna_search(qna_list, query, threshold=70):
    matches = []
    
    # Find matches based on fuzzy string matching
    for entry in qna_list:
        question = entry["q"]
        similarity = fuzz.partial_ratio(query.lower(), question.lower())
        if similarity > threshold:  # Adjust the threshold as needed
            matches.append((entry, similarity))
    
    # Sort matches by similarity (higher similarity first)
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches


# filter and slim down results
def filter_and_search(query, old_card_data_list, tolerance=50):
    # Check if the query is blank or consists of only spaces
    if not query.strip(): 
        return old_card_data_list

    new_card_data_list = []

    # old Levenshtein algorithm
    '''
    for card_data in old_card_data_list:
        for key, value in card_data.items():
            if key != 'target' and (query.lower() in str(value).lower() or
                                    fuzz.token_sort_ratio(
                                            str(value), query) >= tolerance):
                new_card_data_list.append(card_data)
                break
    '''

    for card_data in old_card_data_list:
        for key, value in card_data.items():
            if key != 'target' and query.lower() in str(value).lower():
                new_card_data_list.append(card_data)
                break

    return new_card_data_list
    