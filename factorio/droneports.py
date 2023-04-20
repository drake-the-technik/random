from os import get_terminal_size, system, name


class InvalidBotRatioException(Exception):
    '''
    Raised when logistic and build bot sum in ratio non-equal 7
    '''
    pass


def clear():
    if name == "nt":
        _ = system("cls")
    elif name == "posix":
        _ = system("clear")


def worker(
    droneports_num: int,
    logistic_bots: int,
    build_bots: int,
    bots_ratio: list = [2, 5]
):

    net_capacity_current = {
        "logistic": logistic_bots,
        "build": build_bots
    }

    net_capacity_max = {
        "logistic": droneports_num * bots_ratio[1] * BOT_STACK_SIZE,
        "build": droneports_num * bots_ratio[0] * BOT_STACK_SIZE
    }

    net_capacity_diff = {
        "logistic":
            net_capacity_max["logistic"]
            - net_capacity_current["logistic"],
        "build":
            net_capacity_max["build"]
            - net_capacity_current["build"]
    }

    return {
        "ratio": {
            "logistic": bots_ratio[1],
            "build": bots_ratio[0]
            },
        "logistic": {
            "max": net_capacity_max["logistic"],
            "diff": net_capacity_diff["logistic"]
            },
        "build": {
            "max": net_capacity_max["build"],
            "diff": net_capacity_diff["build"]
            }
    }


DRONEPORT_TOTAL_STACKS = 7
BOT_STACK_SIZE = 50


if __name__ == "__main__":
    clear()
    try:
        while True:
            try:
                droneports_num = int(input("Droneports:\t"))
                print("Currently in logistic network")
                bots_logistic = int(input(" logistic bots:\t"))
                bots_build = int(input(" build bots:\t"))

                while True:
                    try:
                        bots_ratio = input(
                            "Target build/logistic bots ratio: "
                            )
                        bots_ratio = bots_ratio.split('/')
                        bots_ratio = [int(x) for x in bots_ratio]
                        if bots_ratio[0] + bots_ratio[1] != 7:
                            raise InvalidBotRatioException
                        else:
                            break
                    except InvalidBotRatioException:
                        clear()
                        print('Wrong bots ratio!')
                        print(
                            f'Logistic/build bots ratio sum must be'
                            f'equal 7, but'
                            f'{bots_ratio[0]} + {bots_ratio[1]}'
                            f'= {bots_ratio[0]+bots_ratio[1]}'
                            )

                result = worker(droneports_num,
                                bots_logistic,
                                bots_build,
                                bots_ratio)

                clear()
                _header_L = 'Logistic network parameters:'
                _header_R = f'ratio: {bots_ratio[0]} build'\
                    + f'/ {bots_ratio[1]} logistic bots'
                print(_header_L, end='')
                print(
                    f'{_header_R:>{get_terminal_size()[0] - len(_header_L)}}'
                    )
                print('\t\t\tCurrent\t\t  Max\t\tRequired')
                print(f'\tdroneports:\t{droneports_num:5}')
                print(
                    f'\tlogistic bots:\t{bots_logistic:5}'
                    f'\t\t{result["logistic"]["max"]:5}'
                    f'\t\t{result["logistic"]["diff"]:5}'
                    )
                print(
                    f'\tbuild bots:\t{bots_build:5}'
                    f'\t\t{result["build"]["max"]:5}'
                    f'\t\t{result["build"]["diff"]:5}'
                    )

            except ValueError:
                print("Wrong characters in input")

    except KeyboardInterrupt:
        clear()
        print("\r", end='')
