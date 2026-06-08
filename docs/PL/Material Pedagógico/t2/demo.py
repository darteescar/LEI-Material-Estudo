import re

with open("cinema.json", "r") as file:
    text = file.read().splitlines()

print("* Input text:", entry := text[1])

# Search for the movie title
print(re.match(r'"title":\s*".*"', entry)) # match from the beginning, doesn't work
print(re.match(r'.*"title":\s*".*"', entry)) # match from the beginning, catches too much
print(re.match(r'.*"title":\s*".*?"', entry)) # match from the beginning, apparently works, but garbage in the beginning
print(re.search(r'"title":\s*".*?"', entry)) # search anywhere, apparently works

# Search for the movie title if it contains a number
print(re.search(r'"title":\s*".*?\d+.*?"', entry)) # seems to work, it has a number...

print("* Input text:", entry := text[2])

print(re.search(r'"title":\s*".*?\d+.*?"', entry)) # ... but doesn't work if no match
print(re.search(r'"title":\s*"[^"]*?\d+[^"]*?"', entry)) # works, stop at the first "

print("* Input text:", entry := text[1])

print(re.search(r'"title":\s*"[^"]*?\d+[^"]*?"', entry)) # works, stop at the first "
print(re.search(r'"title":\s*"([^"]*?\d+[^"]*?)"', entry)) # capturing group, get only the title text

# Search for all title in the text file
entries = "\n".join(text)
print(re.findall(r'"title":\s*"([^"]*?)"', entries))
print(re.findall(r'"title":\s*"([^"]*?\d+[^"]*?)"', entries))

# Use capturing groups to find titles with repeated patterns
print(re.findall(r'title":\s*"([^"]*?(\w{2})\2[^"]*?)"', entries)) # immediately repeated
print(re.findall(r'title":\s*"([^"]*?(\w{2})\2[^"]*?)"', entries, re.IGNORECASE)) # immediately repeated, ignore case
print(re.findall(r'title":\s*"([^"]*?(\w{5})[^"]*?\2[^"]*?)"', entries)) # repeated anywhere
