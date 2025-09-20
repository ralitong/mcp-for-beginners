import asyncio


# basic boring python function
def hello_printer():
    print(
        "Hi, I am a lowly, simple printer, though I have all I "
        "need in life -- \nfresh paper and my dearly beloved octopus "
        "partner in crime."
    )

# an async def function returns a coroutine object
async def loudmouth_penguin(magic_number: int):
    print(
        "I am a super special talking penguin. Far cooler than that printer."
        f"By the way, my lucky number is: {magic_number}"
    )

def get_random_number():
    # This would be a bad random number generator!
    print("Hi")
    yield 1
    print("Hello")
    yield 7
    print("Howdy")
    yield 4


async def main():
    pass

if __name__ == "__main__":
    # calling a regular function invokes its logic or body
    hello_printer()

    # calling a generator (a function that uses yield) returns a generator object
    generator = get_random_number()
    print(generator)

    # calling next, activate the generator but pauses momentarily
    print(next(generator))
    # should generate 7
    print(next(generator))
    # should generate 4
    print(next(generator))

    # Will throw an error is nothing can be yielded
    # next(generator)

    # calling an async def function returns a coroutine object
    loudmouth_penguin(magic_number=3)
    asyncio.run(loudmouth_penguin(magic_number=3))

    asyncio.run(main())
    print("coroutine main() is done!")

