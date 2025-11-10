import guineajson as G

array = G.fetch("peoples.json")
for person in array:
    print(person["name"], person["age"], person["id"])

print("done")