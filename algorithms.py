def check_coincidences(arr_string, arr):
    if arr_string and arr:
        k = 0
        list_with_counts = []
        for name in arr:
            for letter in name:
                if letter in arr_string:
                    k += 1
            list_with_counts.append((''.join(name), k))
            k = 0
        not_empty = list(filter(lambda x: x[1] != 0, list_with_counts))
        result = list(map(lambda x: x[0], sorted(not_empty, key=lambda x: x[1], reverse=True)))
        print(result)
        return result

