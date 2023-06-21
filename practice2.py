def fibonacci_series():
    number = input('Enter the number of terms you want to generate in the fibonacci series: ')
    integer = int(number)
    fibonacci_list = [0,1]
    for no in range(2,integer):
        next_number = fibonacci_list[no - 1] + fibonacci_list[no - 2]
        fibonacci_list.append(next_number)
    print(fibonacci_list) 


fibonacci_series()
