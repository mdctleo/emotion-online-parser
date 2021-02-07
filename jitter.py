import csv

def create_jitter(file_prefix, sequence):
    with open(file_prefix + '.csv', 'w') as csvfile:
        fieldnames = ['stimFile']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in sequence:
            writer.writerow({'stimFile': 'resources/{file_prefix}_{i}'.format(file_prefix=file_prefix, i=i)})




create_jitter('01F_FE_C',[0,1,2,3,4,5,6,7,7,7,7,8,9,10,
11,12,13,14,14,14,14,15,16,17,18,18,18,19,20,
21,22,23,24,24,24,25,26,27,28,29,30,30,30,30,
31,32,32,32,33,34,35,36,37,37,37,38,39,40,
41,42,43,44,45,46,47,47,47,47,48,49,50,
51,52,53,54,54,54,55,56,57,57,57,58,59,60,
61,62,63,64,65,65,65,66,67,68,69,69,69,69,69,70,
71,72,73,74,75,76,76,76,76,77,78,79,80,
81,81,81,81,82,83,84,85,86,87,88,88,88,89,90,
91,92,93,94,94,94,95,96,97,98,99,100])