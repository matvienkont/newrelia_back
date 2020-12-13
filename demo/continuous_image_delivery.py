from demo.ai_logic import interrupted
import time

def img_delivery():
    print("HEY")
    while not interrupted:
        print("Working hard...")
        time.sleep(3)
        print("All done!")

        if interrupted:
            print("Gotta go")
            break
