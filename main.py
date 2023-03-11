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


# # DATA = input("Enter link/links: ")
# DATA = open("links", "r").read()
# # DATA = "https://nickwignall.medium.com/5-psychological-reasons-you-dont-feel-confident-58d83b4c9d60"
# for url in DATA.splitlines():
#     mediumtomd.save_to_markdown(url)
