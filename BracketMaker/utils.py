def interleave(list1: list, list2: list) -> list:
    """ Takes two lists and interleaves them. If the lists are of different lengths, the
        remaining items from the longer list get appended to the end of the new list
    """
    result = []
    for i in range(max(len(list1), len(list2))):
        if (i < len(list1)):
            result.append(list1[i])
        if (i < len(list2)):
            result.append(list2[i])
    
    return result

def random_choice(choices: list):
    import random
    return random.choice(choices)