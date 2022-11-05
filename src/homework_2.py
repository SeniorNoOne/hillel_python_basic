# task 1
print("Task 1:")
a = 2 * 3
b = (3 * 3 + 8) / 3
c = 8 // 3
d = 8 % 3
e = 5 ** 2
f = 'Hello ' + 'world'
task1 = [a, b, c, d, e, f]

for var in task1:
    print(type(var), '\t', var)
print()


# task 2
print("Task 2:")
string = "Hillel " + 'IT' + " school"
print(string)
print()


# task 3
print("Task 3:")
a = string[:10]
b = string[2:12]
c = string[len(string) - 10:]
d = string[::-1]
e = string[::2]
ee = string[1::2]
task3 = [a, b, c, d, e, ee]

for var in task3:
    print(var)
print()


# task 4
print("Task 4:")
num_1 = float(input("Enter first number: "))
num_2 = float(input("Enter second number: "))
print("Sum of those numbers is: ", num_1 + num_2)
