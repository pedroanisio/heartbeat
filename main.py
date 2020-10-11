import time

beats_filename = "beats.txt"
events_filename = "events.txt"
number_of_lines = 4
diff_threshold = 70


def write_event(event_start,event_end):
    e = open(events_filename, "w")
    e.write(event_start,sevent_end + "\n")
    e.close()


beats_array = []
f = open(beats_filename, "r")
num_lines = sum(1 for line in f)
f.close()

if num_lines > number_of_lines:
    i = 0
    with open(beats_filename, "r") as f:
        for line in (f.readlines()[-number_of_lines:]):
            beats_array.append(float(line))
            i = i + 1
n = len(beats_array) - 1

while n > 0:
    diff = beats_array[n] - beats_array[n - 1]
    if diff > diff_threshold:
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(beats_array[n - 1]))
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(beats_array[n]))
        print(f"skipped {int(diff / 60)} beats from {start_time} to {end_time}")
        write_event(str(beats_array[n - 1]),str(beats_array[n]))
        print("email")

    n = n - 1