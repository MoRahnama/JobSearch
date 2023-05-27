from Functions import *

def main():
    guess_number()
    input_value = int(input("please give a number : "))
    reverse_integer(input_value)
    check_if_binary(input_value)
    check_if_prime(input_value)
    Check_if_Armstrong_number(input_value)
    if input_value < 35:
        generate_Fibonacci (input_value)
    sum_of_digits(input_value)

    print(f"Unique items count: {count_unique_items('abbccd')}")
    s1 = input("please give a String : ")
    s2 = input("please give a Character to remove : ")
    print(f"Toral Number of occurence of {s2} is : {count_char(s1,s2)}")
    print(f"{remove_char(s1,s2)}")
    

if __name__ == "__main__":
     main()