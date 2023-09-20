data = ["Apple", "Banana", "Orange"]
with open("result.txt", "a") as file:
    for item in data:
        file.write(item + "\n")