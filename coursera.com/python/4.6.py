def computepay(h,r):
    pay = h * r
    if (h > 40):
        return pay + (h-40) * 0.5 * r
    return pay

hrs = input("Enter Hours:")
rate = input("Enter Rate:")
p = computepay(float(hrs), float(rate))

print("Pay",p)
