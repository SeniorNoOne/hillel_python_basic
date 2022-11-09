import math

# task 1
a = float(input("A coef: "))
b = float(input("B coef: "))
c = float(input("C coef: "))

d = b ** 2 - 4 * a * c
x1 = (-b + d ** 0.5) / 2 / a
x2 = (-b - d ** 0.5) / 2 / a

if x1 == x2:
    print("x = ", x1)
else:
    print("x1 =", x1)
    print("x2 =", x2)


# bonus task
num_to_flip = int(input("\nEnter num to flip: "))
num_of_digits = int(math.log10(num_to_flip)) + 1
print("Flipped number is: ", end="")

for i in range(num_of_digits):
    print(num_to_flip % 10, end="")
    num_to_flip = int(num_to_flip / 10)
