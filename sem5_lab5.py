from threading import Thread

token = [0, 0, 0]       # p, t, r
frames = []               # AC(3 bit), DA(1 bit), SA(1 bit), INFO, FCS(1 bit), FS(2 bit)
info_to_monitor = [0, 0, 0]


def check_info(SA, info):
    if info[1] == 1:
        if info[4] == SA:
            if info[7] == 1:
                print("OK! Data has been read by recipient!")
            if info[8] == 1:
                print("And data has been copied!")
            info = token
        elif info[3] == SA:
            print("It was data for me({}): {}".format(SA, info[5]))
            FCS = 0
            for nums in info[5]:
                if nums == '1':
                    FCS += 1
            FCS = FCS % 2
            if FCS == info[6]:
                print('Data is correct')

            info[7] = 1
            if info[5][0] == '1':
                info[8] = 1

    if info[1] == 0:
        index = [False, 0]
        for i in range(len(frames)):
            if frames[i][0] > info[0] and frames[i][4] == SA:
                info = frames[i]
                index[0] = True
                index[1] = i
        if index[0]:
            del frames[index[1]]

    return info


def get_info_frame():
    add_frame = 1
    while add_frame == 1:
        try:
            add_frame = int(input('Do you want to send data from some station to another one?\n1-yes\n0-no\n'))
            if add_frame < 0 or add_frame > 1:
                raise ValueError
            if add_frame == 1:
                SA = int(input('From what station do you want to send data: '))
                if SA < 1 or SA > 3:
                    raise ValueError
                info = input('Enter data to send: ')
                DA = int(input('Enter address to send: '))
                if DA < 1 or DA > 3:
                    raise ValueError
                p = int(input('Enter priority (>=1 and <=7): '))
                if p < 1 or p > 7:
                    raise ValueError
                res = []
                FCS = 0
                for nums in info:
                    if nums == '1':
                        FCS += 1

                FCS = FCS % 2
                res.extend([p, 1, 0, DA, SA, info, FCS, 0, 0])
                frames.append(res)
        except ValueError:
            print('Please, enter correct value.')
            add_frame = 1


def third(info):
    print("Received in 3: ", info)
    info = check_info(3, info)
    global info_to_monitor
    info_to_monitor = info


def second(info):
    print("Received in 2: ", info)
    info = check_info(2, info)
    thread3 = Thread(target=third, args=(info,))
    thread3.start()
    thread3.join()


def first(info):
    print("Received in 1: ", info)
    info = check_info(1, info)
    thread2 = Thread(target=second, args=(info,))
    thread2.start()
    thread2.join()


answer = 1
while answer or len(info_to_monitor) != 3:
    if len(info_to_monitor) == 3:
        get_info_frame()
    print("------------------------------------")
    thread1 = Thread(target=first, args=(info_to_monitor,))
    thread1.start()
    thread1.join()
    print('Received monitor: ', info_to_monitor)
    if len(info_to_monitor) == 3:
        answer = int(input('Do you want to send new data?\n1-yes\n0-no\n'))

