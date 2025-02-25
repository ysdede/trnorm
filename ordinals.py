import re

# Compile regex patterns globally for efficiency
pattern = re.compile(r'\b(\d+)\. (\w+)')
seq_pattern = re.compile(r'(\b\d+\.,?)\s+(?=\d+\.)')

# Convert numbers to their textual representation in Turkish
def num_to_text(n):
    num_dict = {
        1: "birinci", 2: "ikinci", 3: "üçüncü", 4: "dördüncü", 5: "beşinci",
        6: "altıncı", 7: "yedinci", 8: "sekizinci", 9: "dokuzuncu", 10: "onuncu",
        11: "on birinci"
    }
    return num_dict.get(n, f"{n}.")

# Check if a word is a keyword that indicates a number should be converted
def check_keyword(word, keywords):
    return any(word.startswith(kw) for kw in keywords)

# Normalize text with compiled regex patterns
def normalize_ordinals(text):
    keywords = {"parmak", "dakika"}

    def repl(m):
        num, keyword = int(m.group(1)), m.group(2)
        if check_keyword(keyword, keywords):
            return f"{num_to_text(num)} {keyword}"
        return m.group(0)

    def seq_repl(m):
        nums = list(map(int, re.findall(r'\d+', m.group(0))))
        return ', '.join(num_to_text(num) for num in nums) + ' '

    text = re.sub(seq_pattern, seq_repl, text)
    return re.sub(pattern, repl, text)
