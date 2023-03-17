from difflib import SequenceMatcher

string1 = "amd ryzen 3 5500"
string2 = "ryzen 5500"

ratio = SequenceMatcher(None, string1, string2).ratio()
print(ratio)  # 0.6666666666666666