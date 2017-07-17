import csv
import sys
if len(sys.argv) < 2:
    print("No file specified.")
    exit()
file_name = sys.argv[1]
if len(sys.argv) < 3:
    out_name = "ACE_calc_" + file_name
else:
    out_name = sys.argv[2]
ACE_dict = {}
out_file = open(out_name, 'w+', newline='')
with open(file_name, newline='') as ATCF_file:
    line_reader = csv.reader(ATCF_file, delimiter=',', quotechar='|')
    line_writer = csv.writer(out_file, delimiter=',', quotechar='|')
    current_storm = None
    ACE = 0
    for line in line_reader:
        if len(line) == 4:
            # Finished with this storm? Commit it to the file.
            if current_storm != None:
                current_storm.append(str(ACE/10000))
                line_writer.writerow(current_storm)
            current_storm = line[:2]
            print("Processing " + str(current_storm))
            ACE = 0
        elif int(line[1]) % 600 == 0: # Only count 6-hourly intervals
            ACE += int(line[6])**2
    # Last storm
    current_storm.append(str(ACE/10000))
    line_writer.writerow(current_storm)
    out_file.close()