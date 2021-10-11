largest = None
smallest = None
while True:
    num = input("Enter a number: ")
    if num == "done" : break
    #print(num)
    try:
        num = int(num)
    except:
        print("Invalid input")
        continue
    if largest is None:
        largest = num
        smallest = num
    if num > largest:
        largest = num
    if num < smallest:
        smallest = num

print("Maximum","is", largest)
print("Minimum","is", smallest)
