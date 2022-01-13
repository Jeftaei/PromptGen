from typing import Dict, List
import time

blacklistedChars = ["x", "z", "j", "q"] # list of characters that will not appear in prompts

# adapted from my wbm bot, useless for this project but cool anyway
def SolvePrompt(prompt: str, wordlist: list) -> List[str]:
    """Solves the `prompt` with the `wordlist`"""
    return [word for word in wordlist if prompt.lower() in word]

def AsPercent(amount: int, total: int) -> float:
    """return the float of `amount` divided by `total`, if `total` is 0 return `0.0`"""
    return amount/total * 100 if total != 0 else 0.0

def clamp(value, minv, maxv) -> int:
    return max(min(value, maxv), minv)

def GetWordlist(dirPath: str) -> List[str]:
    """Grab text file from `dirpath` and turns it into a list of words"""
    with open(dirPath, "r") as f:
        wordlist = f.read().lower().split("\n")
    return wordlist

def CheckString(string: str) -> bool:
    """if valid `string` return `True`, else return `False`"""
    
    # check for blacklisted characters and return the bool
    return not any([x in string for x in blacklistedChars])

# formatting in the file to look nice
def FormatPrompt(prompt: str, charFreq: float) -> str:
    # 😃 👍
    if len(prompt) == 1:
        prompt += "  "
    elif len(prompt) == 2:
        prompt += " "
    return f"{prompt}  |  Frequency: {charFreq}%\n"

def PromptFrequency(d: dict) -> Dict[str, float]:
    """Returns a frequency chart of the supplied `d` dict with percent values"""
    return {k:round(AsPercent(d[k], sum(d.values())), 4) for k in d.keys()} # this looks better but still pretty ugly

def WriteToFile(Final: dict, freq: dict, sortby: str = "prompt") -> None:
    """Creates a text file for GenerateAllPrompts and writes data, sorts by `sortby` which defaults to prompt"""
    with open("test3.txt", "w") as f:
        f.write(f"List of all valid prompts (1-3 letters only) and their frequency of appearing as a percent | Blacklisted Characters: {blacklistedChars} | Sorted by {sortby}\n\n")
    
        if sortby == "prompt":
            for i in Final.keys():
                f.write(FormatPrompt(i, freq[i]))
        elif sortby == "frequency":
            freq = dict(sorted(freq.items(), key = lambda x:x[-1], reverse=True)) # sorts the dictionary by value in descending order
            for i in freq:
                f.write(FormatPrompt(i, freq[i]))

def GetSubStrings(word: str, promptLength: int) -> List[str]:
    """Gets all substrings of a given `word` that are of `promptLength` length"""
    # thanks sev for making this look much nicer (and also take way less time and overall be better), but i ruined it anyway. 👍
    # temp = []

    # for i in range(len(word)):
    #     for j in range(i+1, min(len(word)+1, i+promptLength+1)):
    #         temp.append(word[i:j])

    # return list(set(temp))
    return list(set([word[i:j] for i in range(len(word)) for j in range(i+1, min(len(word)+1, i+promptLength+1))])) # ahahah


def GenerateAllPrompts(promptLength: int) -> None:
    """Creates a text file with all prompts equal to `promptLength` and their frequency of appearing"""
    wordlist = GetWordlist("dict/master.txt") # change this to the path for the dictionary
    s = {}

    for word in wordlist:
        for substring in GetSubStrings(word, promptLength):
            if CheckString(substring):
                if substring not in s.keys():
                    s[substring] = 0
                else:
                    s[substring] += 1

    unique = s.keys()
    WriteToFile(unique, PromptFrequency(s), sortby="frequency")

start = time.time()
GenerateAllPrompts(3)
print(f"Took: {time.time() - start}")