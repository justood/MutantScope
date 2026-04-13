def find(ordered_list, element_to_find):
    start_index = 0
    end_index = len(ordered_list) - 1

    while start_index <= end_index:
        middle_index = (start_index + end_index) // 2
        middle_element = ordered_list[middle_index]

        if middle_element == element_to_find:
            return True
        elif middle_element < element_to_find:
            start_index = middle_index + 1
        else:
            end_index = middle_index - 1

    return False

# if __name__=="__main__":

#   l = [2, 4, 6, 8, 10]

#   print(find(l, 5)) # prints False

#   print(find(l, 10)) # prints True

#   print(find(l, -1)) # prints False

#   print(find(l, 2)) # prints True
