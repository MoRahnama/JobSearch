# Functions

def reverse_integer (Input):
    """
    This is a function for reversing an Input we get from the user and returing the reversed Input
    """
    reversed_Input = 0
    while Input!= 0:
        reversed_Input = reversed_Input*10 + Input%10
        Input //= 10
    print(f"The reversed number is {reversed_Input}")
    return reversed_Input

def count_digits (Input):
    """
    This is a function for counting and returing how many digits the Input has
    """
    digit_count = 0
    while Input!= 0:
        digit_count += 1
        Input //= 10
    print(f"Your Input has {digit_count} digits")
    return digit_count

def Fibonacci (Input):
    """
    This is a function for generating the the Fibonacci series using a recursive function
    """
    if Input == 0:
        return 0
    elif Input == 1:
        return 1
    else:
        return Fibonacci(Input - 1) + Fibonacci (Input - 2) 

def generate_Fibonacci (Input):
    """
    This is a function for generating the Fibonacci series to the Input value 
    """
    print(f"The Fibonacci series unitl {Input}:")
    for i in range(0,Input):
        if (Fibonacci(i) < Input):
            print(Fibonacci(i), end=' ')

def check_if_prime (Input):
    """
    This is a function for checking if the Input number is prime or not 
    """
    i = 0
    for i in range(2,Input//2):
        if  Input%i == 0:
            print(f"Your number is not prime")
            break
    else:
        print(f"Your number is prime")

def check_if_prime (Input):
    """
    This is a function for checking if the Input number is prime or not 
    """
    i = 0
    for i in range(2,Input//2):
        if  Input%i == 0:
            print(f"Your number is not prime")
            break
    else:
        print(f"Your number is prime")    


def Check_if_Armstrong_number (Input):
    """
    This is a function for checking if the Input number is Armstrong
    """
    digit_count = count_digits(Input)
    Original = Input
    Armstrong = 0

    while Input!= 0:
        Armstrong += (Input % 10) ** digit_count
        Input //= 10

    if  Armstrong == Original:
        print(f"Your number is Armstrong")
    else:
        print(f"Your number is not Armstrong")


def check_if_binary (Input):
    """
    This is a function for checking if the Input number is binary or not 
    """
    while(Input>0):
        Modulus = Input % 10
        if Modulus != 0 and Modulus != 1:
            print(f"Your number is not binary")
            break
        Input //= 10
        if Input == 0:
            print(f"Your number is binary")

def sum_of_digits (Input):
    """
    This is a function for calculating the sum of all the digits of the input
    """
    Sum = 0
    while(Input>0):
        Sum += Input % 10
        Input //= 10
    print(f"The sum of all the digits of your number is {Sum}")

def count_unique_items(sequence):
    unique_items = []
    unique_count = 0
    for item in sequence:
        if item not in unique_items:
            unique_items.append(item)
            unique_count += 1
    return unique_count
        
