import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

words = {}

# I'm breaking these regezes in pieces to make debugging easier, instead of
# defining multiple capture groups for the entire syslog line at once
date_regex = r"^(^[\s\d\w]+\s+\d+:\d+:\d+)"

username_regex = r"^.*\d+:\d+:\d+\s+(\S+)\s+"

program_regex = r"^.*\d+:\d+:\d+\s+\S+\s+([\w\./-]+)"

pid_regex = r"[\w\./-]+\[(\d+)\]:"

message_regex = r"^.*\d+:\d+:\d+\s+\S+\s+[\w\./-]+\[?\d*\]?\(?[a-zA-Z0-9=]*\)?:\s+(.*)"

file = open('/var/log/syslog', 'r')

# read line by line in case the file is large
for line in file:

    line = file.readline().strip()

    # deal with the blank line at the end
    if not line:
        continue

    username_search = re.search(username_regex, line)
    username = username_search.group(1)

    program_search = re.search(program_regex, line)
    program = program_search.group(1)

    try:
        pid_search = re.search(pid_regex, line)
        pid = pid_search.group(1)
    except AttributeError:
        # probably no pid
        pid = None

    message_search = re.search(message_regex, line)
    message = message_search.group(1)

    try:
        words[username] += 1
    except KeyError:
        words[username] = 1

    try:
        words[program] += 1
    except KeyError:
        words[program] = 1

    if pid:
        try:
            words[pid] += 1
        except KeyError:
            words[pid] = 1

file.close()

print(words)

wc = WordCloud(background_color="black",
               width=1000,
               height=1000,
               max_words=100,
               relative_scaling=0.5,
               normalize_plurals=False).generate_from_frequencies(words)
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
