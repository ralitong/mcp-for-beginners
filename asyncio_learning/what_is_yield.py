# yield returns a value, but does not
# terminate the function unlike `return`
def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1


if __name__ == "__main__":

    for number in count_up_to(5):
        print(f"Yielding {number} ...")