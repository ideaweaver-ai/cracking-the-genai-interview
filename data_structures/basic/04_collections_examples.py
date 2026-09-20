"""Run all examples or one: python collections_examples.py dictionaries"""


def lists():
    scores = [10, 30, 20]
    scores.append(40)
    removed = scores.pop()
    scores.sort()
    print(scores[0], scores[1:], removed)


def dictionaries():
    text = "banana"
    counts = {}
    for letter in text:
        counts[letter] = counts.get(letter, 0) + 1
    print(counts, "b" in counts)


def sets():
    attendees = {"Ada", "Lin", "Ada"}
    attendees.add("Mina")
    attendees.remove("Lin")
    print(attendees, "Mina" in attendees)


def tuples():
    coordinate = (37.77, -122.42)
    locations = {coordinate: "San Francisco"}  # Immutable tuples can be dict keys.
    print(locations[coordinate])


EXAMPLES = {"lists": lists, "dictionaries": dictionaries, "sets": sets, "tuples": tuples}

if __name__ == "__main__":
    import sys

    for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
        EXAMPLES[example]()
