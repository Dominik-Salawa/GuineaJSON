import guineajson as G
import random     as R

names = [
    [
        "Liam", "Olivia", "Noah", "Emma", "Ava", "Isabella", "Sophia", "Mason", "Logan", "Lucas",
        "Ethan", "Mia", "Amelia", "Harper", "Evelyn", "Charlotte", "Abigail", "Ella", "Jackson", "Aiden",
        "Caden", "Grayson", "Aria", "Scarlett", "Victoria", "Madison", "Lily", "Aurora", "Hannah", "Zoe",
        "Gabriel", "Benjamin", "Elijah", "James", "Michael", "Alexander", "Daniel", "Matthew", "Henry", "Sebastian"
    ],
    [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
        "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
    ]
]

addr = "peoples.json"

G.__default__ = []          # If we didn't re-assign, it would be `None`
array = G.fetch(addr, throws_errors=False, return__default__if_empty=False) # Will now return `[]` if it encounters a problem (also no errors will be thrown)

if array == None: # If it turns out `peoples.json` is empty, for demo purposes, we set `return__default__if_empty` to false
    array = G.__default__
    print(f"`{addr}` was empty!")
print()
print(array)
input("\nThis is the array above, press enter to continue...")

def id_exists(id):
    for person in array:
        if person["id"] == id: return True
    return False

for i in range(20000):
    fn  = names[0][R.randint(0, (len(names[0]) - 1))]
    ln  = names[1][R.randint(0, (len(names[1]) - 1))]
    age = R.randint(0, 100)
    id  = R.randint(100000000, 999999999)

    while True:
        if id_exists(id):
            print(f"Conflicting IDs!\nConflicter: {(fn + " " + ln)} ({id})")
            for person in array:
                if person["id"] == id:
                    print(f"Victim: {person["name"]} ({person["id"]})")
                    break 
            id = R.randint(100000000, 999999999)
        else: break

    array.append({"name": (fn + " " + ln), "age": age, "id": id})
    print((fn + " " + ln), age, id)

G.save(array, addr, overwrite=True, throws_errors=True, space_count=10, dont_save_if_malformed_JSON=True)
print("Done")