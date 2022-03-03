def main():
    while True:
        time.sleep(0.05)
        if msvcrt.kbhit():
            print(msvcrt.getch())
        
if __name__ == "__main__":
    import msvcrt
    import time
    main()

