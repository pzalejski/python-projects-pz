import random, string


def generate(length):
    password = "".join(random.SystemRandom().choice(string.ascii_letters + string.punctuation + string.digits) for _ in range(length))
    return password

def check(password):
    lower = sum(1 for letter in password if letter.islower())
    upper = sum(1 for letter in password if letter.isupper())
    digit = sum(1 for letter in password if letter.isnumeric())
    special = sum(1 for letter in password if letter in string.punctuation)

    if lower > 0 and upper > 0 and digit > 0 and special > 0:
        return True
    else:
        return False


def main():
    print("[*] Remember that a strong password should be longer than 8 characters!")
    length = input("[*] Enter how long you would like oyur password to be: ")
    if length.isdigit():
        length = int(length)
    else:
        print("[*] Enter a number! ")

    if length <= 3:
         print("[*] Not possible to generate the password. Please use a longer one. ")
    else:
        password_str = False
        while not password_str:
            password = generate(length)
            password_str = check(password)
        print("[*] Your password has been generated " + "".join(password))


if __name__ == "__main__":
    main()
