import asyncio
import builtins
import pickle

async def cycle():
    counter = 0
    while True:
        if counter == 0:
            shared = {"interrupted": "False"}
            with open("../cfg.pickle", "wb") as handle:
                pickle.dump(shared, handle)

        await asyncio.sleep(4)
        counter += 1

        if counter > 10:
            shared = {"interrupted": "True"}
            with open("../cfg.pickle", "wb") as handle:
                pickle.dump(shared, handle)
            counter = 0
            await asyncio.sleep(10)
        print(counter)



def main():
    asyncio.run(cycle())

if __name__ == "__main__":
    main()
