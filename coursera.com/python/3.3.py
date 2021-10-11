score = input("Enter Score: ")
sc = float(score)

if sc > 1:
    print("Invalid value")
elif sc >= 0.9:
    print("A")
elif sc >= 0.8:
    print("B")
elif sc >= 0.7:
    print("C")
elif sc >= 0.6:
    print("D")
elif sc >= 0:
    print("F")
else:
    print("Invalid value")

