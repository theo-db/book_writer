import network as Network
import numpy

network = Network.loadNetwork("network.nnetwork")

codes = "abcdefghijklmnopqrstuvwxyz \".,?!';:()/\\0123456789"
chars_in = int(network.layers[0]/len(codes))
chars_out = int(network.layers[-1]/len(codes))

text = ""
while len(text) < chars_in:
    text=""
    text = input("enter at least {} characters to begin the story:\n\n".format(chars_in))
    t = list(text.lower())
    for i in range(len(t)-1,-1,-1):
        if t[i] not in codes:
            del t[i]
    text = "".join(t)
string = text[-chars_in:]

def from_string(s):
    values = numpy.zeros(chars_in*len(codes), numpy.float64)
    for i in range(chars_in):
        ind = codes.index(s[i])
        values[i*len(codes) + ind] = 1.0
    return values

def to_string(values):
    v = values.reshape(chars_out, len(codes))
    out = ""
    for i in v:
        ind = i.tolist().index(max(i))
        char = codes[ind]
        out += char
    return out

data = from_string(string)
for i in range(100):
    values = network.use(data)
    s = to_string(values)
    text += s
    new_string = text[-chars_in:]
    data = from_string(new_string)

print(text)
    
