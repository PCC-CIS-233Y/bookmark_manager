from input_validation import input_int, y_or_n, input_string, select_item, input_item, valid_g_number


def valid_g_number(n):
    return len(n) == 9 and n[0] == 'G' and n[1:9].isdigit()

"""
age = input_int("How old are you? ", error="Age must be a whole number, between 0 and 119!", ge=0, lt=120)
print(age)
year = input_int("What year were you born: ", "Must be a year between 1901 and 2024!", gt=1900, le=2024)
print(year)

print(y_or_n("Do you like Python (y/n)? "))

print(input_string("What is your name? "))
# G01111111
def valid_g_number(n):
    return len(n) == 9 and n[0] == 'G' and n[1:9].isdigit()

print(input_string("What is your G#? ", "G# must be 9 characters long, start with G, and be all digits after that.", valid_g_number))

day = select_item(
    "What day is it? ",
    "Must be a day of the week!",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    {
        "M": "Monday",
        "Tu": "Tuesday",
        "W": "Wednesday",
        "Th": "Thursday",
        "F": "Friday",
        "Sa": "Saturday",
        "Su": "Sunday"
    })
print(day)
print(select_item())
"""
print(input_item("int", "How old are you? ", error="Age must be a whole number, between 0 and 119!", ge=0, lt=120))
print(input_item("y_or_n", "Do you like Python (y/n)? "))
print(input_item("string", "What is your G#? ", "G# must be 9 characters long, start with G, and be all digits after that.", valid_g_number))
print(input_item(
    "select",
    "What is your favorite fruit? ",
    "Must be apple, banana, or cherry!",
    ["Apple", "Banana", "Cherry"],
    {
        "a": "Apple",
        "b": "Banana",
        "c": "Cherry"
    }))
