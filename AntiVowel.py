def anti_vowel(text):
    t = " "
    for v in text:
        for i in "ieaouIEAOU":
            if v == i:
                v = " "
            else:
                v = v
        t = t + v
    return t


print anti_vowel("Hey You!")
print anti_vowel("Hey look Words!")
print anti_vowel("aeiouAEIOU")