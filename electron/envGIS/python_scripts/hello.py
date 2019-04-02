from time import sleep as sleep
import sys



def main(num):
    message = int(num)**2
    print(message)

if __name__ == "__main__":
    a = sys.argv[1]
    main(a)