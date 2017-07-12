import cs50

def main():
    while True:
        print("How much change is owed?")
        amt = cs50.get_float()
        if amt >= 0:
            break
    
    n = 0
    c = int(round(amt * 100))
    
    n += c // 25
    c %= 25
    
    n += c // 10
    c %= 10
    
    n += c // 5
    c %= 5
    
    n += c
    
    print("{}".format(n))
    
if __name__ == "__main__":
    main()