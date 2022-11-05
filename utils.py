import csv
from codeforces_api import get_rating


def get_handles():
    res = []
    with open("handles.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            res.append(row["handle"])
    return res


def update_rating():
    handles = []
    with open("handles.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            handles.append(row["handle"])
    rating = get_rating(handles)
    header = ["handle", "rating"]
    with open('handles.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for r,h in zip(rating, handles):
            writer.writerow({"handle": h, "rating": r})

if __name__ == "__main__":
    update_rating()