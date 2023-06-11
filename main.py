from subprocess import check_call, CalledProcessError
import os
import sys

CEND = "\33[0m"
CBEIGE = "\33[36m"
CRED = "\33[31m"
CGREEN = "\33[32m"


def evaluate(word, pattern):
    score = 0
    for c in word:
        if c in pattern:
            score += 1
    return score


def predict(word, array):
    best_word = ""
    best_score = 0
    for each in array:
        score = evaluate(word, each)
        if score > best_score:
            best_score = score
            best_word = each
    return best_word, best_score


baseDir = os.path.dirname(os.path.abspath(__file__))
profiles = [
    x.replace(".compose.yaml", "")
    for x in os.listdir(os.path.join(baseDir, "profiles"))
    if x.endswith(".compose.yaml")
]
args = sys.argv

description = (
    f"# Use {CBEIGE}docker compose{CEND} from repository\n\nAvailable compose files:\n"
)
for s in profiles:
    description += f" - {s}\n"

if len(args) < 2:
    print(end="\n")
    print(description)
    sys.exit()

if args[1] not in profiles:
    print(f"{CRED}{args[1]}{CEND} is not recognized as a compose file.", end=" ")

    sugguestion, confidence = predict(args[1], profiles)
    if confidence > 0:
        print(f"Maybe you meant {CGREEN}{sugguestion}{CEND}", end="")
    print(end="\n")
    sys.exit()

compose_file = os.path.join(baseDir, "profiles", args[1] + ".compose.yaml")
if not os.path.isfile(compose_file):
    print(f"{CRED}{compose_file}{CEND} is not found.")
    sys.exit()
try:
    command = ["docker", "compose", "-f", compose_file]
    command += args[2:]
    check_call(command, shell=True)
except (CalledProcessError, KeyboardInterrupt) as e:
    pass
