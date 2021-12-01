import pickle
import argparse

DESCRIPTION = '''
Desc
'''


class InterestsStore:
    def __init__(self):
        self._interests = []

    def append(self, interest):
        if not self.find(interest.name):
            self._interests.append(interest)
            self._sort()

    def find(self, name):
        for i in self._interests:
            if i.name == name:
                return i
        return None

    def remove(self, name):
        pass

    def count(self):
        return len(self._interests)

    def __repr__(self):
        self._sort()
        msg = ""
        for i, it in enumerate(self._interests):
            msg = msg + "[{}]: {}\n".format(str(i + 1), str(it))
        return msg

    def _sort(self):
        self._interests.sort(key=lambda x: x.total_time)


class Interest:
    def __init__(self, name):
        self.name = name
        self.logged_times = []
        self.total_time = 0

    def __str__(self):
        return self.name + " (Logged {} minutes)".format(self.total_time)

    def log_time(self, minutes):
        self.logged_times.append(minutes)
        self.total_time = self.total_time + minutes


def add_interest(name, store):
    interest = Interest(name)
    store.append(interest)


def log_time(store, interest_name, time):
    interest = store.find(interest_name)
    interest.log_time(time)


def retire(interest_name):
    interests_store.remove(interest_name)


def load():
    try:
        with open("fuzzy_tt.pickle", "rb") as f:
            interests_store = pickle.load(f)
    except FileNotFoundError:
        interests_store = InterestsStore()
    return interests_store


def save(store):
    with open("fuzzy_tt.pickle", "wb") as f:
        pickle.dump(store, f)

def run(args):
    interest_store = load()

    if args.add:
        add_interest(args.add, interest_store)
    elif args.show:
        print(interest_store)
    elif args.log and args.interest:
        log_time(interest_store, args.interest, args.log)
    else:
        print("Invalid argument combination!")

    save(interest_store)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-a', '--add', help='Add a new interest')
    parser.add_argument('-s', '--show', help='Show current interests', action='store_true')
    parser.add_argument('-l', '--log', type=int, help='Spent time in minutes')
    parser.add_argument('-i', '--interest', help='Interest to log time against')
    args = parser.parse_args()
    run(args)

