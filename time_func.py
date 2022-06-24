import time

def timeit(count=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()

            for i in range(count):
                func(*args, **kwargs)

            end_time = time.time()
            print(f'{func.__name__} took {(end_time - start_time) / count} seconds')

        return wrapper
    return decorator


# @timeit(count=5) 
# def long_function(time_to_sleep):
#     time.sleep(time_to_sleep)
#     return "done"


# if __name__ == '__main__':
#     print(long_function(1))