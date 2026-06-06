def swap_case(s):
    swap= []
    for i in s:
        if i.isalpha():
            if i.islower():
                i = str.upper(i)
                swap.append(i)
                continue
            else:
                i = str.lower(i)
                swap.append(i)
                continue
        else:
            swap.append(i)
    return ''.join(swap)

if __name__ == '__main__':
    s = input()
    result = swap_case(s)
    print(result)