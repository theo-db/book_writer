files = [
    "books/a_christmas_carol.txt",
    "books/dr_jekyll_and_mr_hyde.txt",
    "books/frankenstein.txt",
    "books/hound_of_the_baskervilles.txt",
    "books/oliver_twist.txt",
    "books/sherlock_holmes.txt",
    "books/time_machine.txt",
    "books/treasure_island.txt",
    "books/wizard_of_oz.txt"
    ]

codes = "abcdefghijklmnopqrstuvwxyz \".,?!';:()/\\0123456789"
chars_in = 100
chars_out = 1

shape = [chars_in * len(codes),
         20,45,100,
         chars_out * len(codes)]

import network as Network
import numpy, random, threading

random.shuffle(files)

network = Network.Network(shape)

try:
    #train one book at a time so the RAM won't hate me
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
        #for x in range(total_iterations):
        #    v = x/total_iterations
        #    if v > passed+0.01:
        #        print("{}%".format(v*100))
        #        passed += 0.01
        #    data = []
        #    output = []
        #    for y in range(iterations):
        range_start = random.randrange(0, len(text)-chars_in-chars_out-1 - iterations, iterations)
        range_end = random.randrange(range_start, len(text)-chars_in-chars_out-1, iterations)
        #so it isn't always in the same range
        #normally would be range(0,len(text)-chars_in-chars_out-1,iterations)
        for x in range(range_start, range_end, iterations):
            data = []
            output = []
            v = x/(len(text)-chars_in-chars_out)
            if v > passed+0.01:
                print("{}%".format(v*100))
                passed += 0.01
            for y in range(iterations):
                #index = random.randrange(len(text) - chars_in - chars_out)
                index = x+y
                input_data = text[index : index+chars_in]
                desired_output_data = text[index+chars_in : index+chars_in+chars_out]
                if len(desired_output_data) < chars_out:
                    desired_output_data += " "*(chars_out-len(desired_output_data))

                in_values = numpy.zeros(shape[0], numpy.float64)
                for i in range(chars_in):
                    ind = codes.index(input_data[i])
                    in_values[i*len(codes) + ind] = 1.0

                out_values = numpy.zeros(shape[-1], numpy.float64)
                for i in range(chars_out):
                    try:
                        ind = codes.index(desired_output_data[i])
                    except:
                        print("#################################################")
                        print(i)
                        print(desired_output_data)
                        print(len(desired_outoput_data))
                        print(desired_output_data[i])
                        print("#################################################")
                    out_values[i*len(codes) + ind] = 1.0

                data.append(in_values)
                output.append(out_values)
            t = threading.Thread(target=network.train, args=(data, output, iterations))
            t.start()
            t.join()
except KeyboardInterrupt:
    Network.saveNetwork(network, "network.nnetwork")

        
        

    
    

    
    
