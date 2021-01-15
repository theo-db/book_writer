files = [
    "books/a_christmas_carol.txt",
    "books/a_study_in_scarlet.txt",
    "books/dr_jekyll_and_mr_hyde.txt",
    "books/dracula.txt",
    "books/frankenstein.txt",
    "books/gullivers_travels.txt",
    "books/hound_of_the_baskervilles.txt",
    "books/moby_dick.txt",
    "books/oliver_twist.txt",
    "books/sherlock_holmes.txt",
    "books/time_machine.txt",
    "books/treasure_island.txt",
    "books/war_of_the_worlds.txt",
    "books/wizard_of_oz.txt",
    ]

codes = "abcdefghijklmnopqrstuvwxyz \".,?!';:()/\\0123456789"
chars_in = 100
chars_out = 1

random_range = False

shape = [chars_in * len(codes),
         20,45,100,
         chars_out * len(codes)]

import network as Network
import numpy, random, threading

random.shuffle(files)

#network = Network.Network(shape)
network = Network.loadNetwork("network.nnetwork")

try:
    for filename in files:
        print("opening {}".format(filename))
        text = ""
        file = open(filename, encoding="utf8")
        lines = file.readlines()
        file.close()

        for line in lines:
            t = line.replace("\n","").lower()
            t = list(t)
            for i in range(len(t)-1,-1,-1):
                if t[i] not in codes:
                    del t[i]
            t = "".join(t)
            text += t

        text = ' '.join(text.split())

        iterations = 10
        total_iterations = 1000
        passed = -0.01
        if random_range:
            range_start = random.randrange(0, len(text)-chars_in-chars_out-iterations - (iterations*2), iterations)
            range_end = random.randrange(range_start, len(text)-chars_in-chars_out-iterations, iterations)
        else:
            range_start=0
            range_end = len(text)-chars_in-chars_out-iterations
        for x in range(range_start, range_end, iterations):
            data = []
            output = []
            v = x/(len(text)-chars_in-chars_out)
            if v > passed+0.01:
                print("{}%".format(v*100))
                passed += 0.01
            for y in range(iterations):
                index = x+y
                input_data = text[index : index+chars_in]
                desired_output_data = text[index+chars_in : index+chars_in+chars_out]
                if len(desired_output_data) < chars_out:
                    desired_output_data += " "*(chars_out-len(desired_output_data))
                if len(input_data) < chars_in:
                    input_data += " "*(chars_in-len(input_data))

                in_values = numpy.zeros(shape[0], numpy.float64)
                for i in range(chars_in):
                    ind = codes.index(input_data[i])
                    in_values[i*len(codes) + ind] = 1.0

                out_values = numpy.zeros(shape[-1], numpy.float64)
                for i in range(chars_out):
                    ind = codes.index(desired_output_data[i])
                    out_values[i*len(codes) + ind] = 1.0

                data.append(in_values)
                output.append(out_values)
            t = threading.Thread(target=network.train, args=(data, output, iterations))
            t.start()
            t.join()
except:
    pass

Network.saveNetwork(network, "network.nnetwork")
print("saved")
