import pickle
import random


def review_writer(user_curdata):
    review_list=[]
    fileobj = open('reviews.dat', 'ab')
    name = user_curdata.uname
    review = input('Reviews - ')
    review_list.append(name), review_list.append(review)
    pickle.dump(review_list, fileobj)

    fileobj.close()


def review_reader(n,user_curdata):
    fileobj = open('reviews.dat', 'rb')
    output = []
    try:
        while True:
            output_raw = pickle.load(fileobj)
            output.append(output_raw)
    except EOFError:
        fileobj.close()
    if len(output) < n:
        print("Let's write some first! ")
        return review_writer(user_curdata)
    else:
        print("----------------------------------------------------------------\nYour thoughts make us better!\n")
        for i in range(0,n):
            num = random.randint(0, len(output) - 1)
            print(f'{output[num][0]}: {output[num][1]}')
            output.pop(num)
        print('----------------------------------------------------------------\n')


def review_number():
    fileobj = open('reviews.dat', 'rb')
    output = []
    try:
        while True:
            output.append(pickle.load(fileobj))
    except EOFError:
        fileobj.close()
    return len(output)
