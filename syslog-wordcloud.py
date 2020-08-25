import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

words = {}

# exclude the date from a syslog line and just get the rest
excl_date_regex = r"^[A-Za-z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} (.*)"

# extract the username from a syslog line where the date has been filtered out
extract_username_regex = r"^([a-zA-Z0-9._-]+)\s+.*"

extract_prog_regex = r"^[a-zA-Z0-9._-]+\s+([a-zA-Z0-9._-]+)\(?([a-z=]+)?\)?(\[\d+\])?\]?\:"

file = open('/var/log/syslog', 'r')

no_date = ''

# read line by line in case the file is large
for line in file:

    line = file.readline().strip()

    try:
        # filter out date and just get the rest
        date_search = re.search(excl_date_regex, line)
        no_date = str(date_search.group(1))
    except AttributeError:
        pass

    # extract this stuff piece by piece until we get to the message to make
    # troubleshooting quirky syslog lines a bit easier

    # get the user
    username_regex = re.search(extract_username_regex, no_date)
    try:
        words[username_regex.group(1)] += 1
    except KeyError:
        words[username_regex.group(1)] = 1

    print(no_date)
    print(words)

    # get the program name
    program_regex = re.search(extract_prog_regex, no_date)
    try:
        words[program_regex.group(1)] += 1
    except KeyError:
        words[program_regex.group(1)] = 1

file.close()

print(words)

wc = WordCloud(background_color="white",
               width=1000,
               height=1000,
               max_words=10,
               relative_scaling=0.5,
               normalize_plurals=False).generate_from_frequencies(words)
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
