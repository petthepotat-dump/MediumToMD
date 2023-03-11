import os
import mediumtomd

# check if product exists
if not os.path.exists("product"):
    os.mkdir("product")

# ----------------------------------
# actual loop

while True:
    # ask user for file input or url
    option = input("Enter [1-file], [2-url]: ")
    if option == "1":
        # file input
        file = input("Enter file name: ")
        with open(file, "r") as f:
            data = f.read()
        for url in data.splitlines():
            mediumtomd.save_to_markdown(url)
    elif option == "2":
        # url input
        url = input("Enter url: ")
        mediumtomd.save_to_markdown(url)
    else:
        break
