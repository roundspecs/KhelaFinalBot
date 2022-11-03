import csv
def get_handles():
    header = ['handle']
    res = []
    with open('handles.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            res.append(row['handle'])
    return res