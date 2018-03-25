def remove_duplicates(inputlist):
    if inputlist == []:
        return []
    inputlist = sorted(inputlist) # Sort the input list from low to high
    outputlist = [inputlist[0]]# Initialize the output list, and give it the first value of the now-sorted input list

    # Go through the values of the sorted list and append to the output list
    # ...any values that are greater than the last value of the output list
    for i in inputlist:
        if i > outputlist[-1]:
            outputlist.append(i)

    return outputlist


print remove_duplicates([1, 1, 2, 2])
print remove_duplicates(["Ioana", "ioana", "maria", "maria", "Sarah"])