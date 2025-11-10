import guineajson as G

original  = '{"root":[{"id":1,"values":[0,1,{"nested":[2,3,{"deeper":[4,5,{"even_deeper":[6,7,{"x":[8,9,10,{"y":[11,12,{"z":[13,14,15,{"end":["final",16,17,18,{"last":{"a":19,"b":20,"c":[21,22,{"d":[23,24,{"e":["done",25]}]}]}}]}]}]}]}]}]}]}]}]}'
pythonified = G.stringfetch(original, False)
challenge = G.tojson(pythonified, False, space_count=15)

new = "" # rm spaces after the colon `{"root": ...}
for char in challenge:
    if char != " ": new += char
challenge = new

print("ORIGINAL:\n" + original + "\n")
print("TO PYTHON:\n" + str(pythonified) + "\n")
print("RE-CONVERTED:\n" + challenge + "\n")
print("Is the same?:", original == challenge)