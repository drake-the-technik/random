from math import ceil
from os import get_terminal_size, name, system


def clear():
    if name == "nt":
        _ = system("cls")
    elif name == "posix":
        _ = system("clear")


def power_calculation(_users) -> dict:

    if type(_users) is not list:
        facility_power = _users
    else:
        facility_power = 0
        for i in _users:
            facility_power += i[0]["power"] * i[1]
        facility_power = round(facility_power, 3)  # MW/sec

    # MJ for night running
    facility_night_req = facility_power * (TOD["night"] + TOD["transition"])

    additional_power = round(
        facility_night_req / (TOD["midday"] + TOD["transition"]), 3)

    total_power = facility_power + additional_power

    # round power production to whole number of solar panels
    if total_power % ELECTRICITY["solar_panel"]["power"]:
        total_power = round(ELECTRICITY["solar_panel"]["power"]
                            * ceil(total_power
                            / ELECTRICITY["solar_panel"]["power"]), 3)
        additional_power = round(total_power - facility_power, 3)

    power_add_to_max_ratio = additional_power / total_power

    # Power production during day is not 100%, it is linearly grows
    # and falls during sunrise and sunset accordingly
    # only free power directed to the accumulators, thereforce,
    # charging process starts only when produced power > consumed power,
    # and grows to 100% linearly too,
    # until sunrise is over (or falls to 0% in sunset)
    energy_produced = additional_power \
        * (TOD["midday"] + power_add_to_max_ratio * TOD["transition"]) \
        / TICKS_PER_SECOND
    energy_consumed = facility_power \
        * (TOD["night"] + (1 - power_add_to_max_ratio) * TOD["transition"]) \
        / TICKS_PER_SECOND

    return {
        "power": {
            "units": ceil(round(total_power
                                / ELECTRICITY["solar_panel"]["power"], 3)),
            "total": total_power,
            "facility": facility_power,
            "storage": round(max(total_power - facility_power, 0), 3)
        },
        "energy": {
            "cons": round(energy_consumed, 3),
            "cons_units": ceil(
                round(energy_consumed
                      / ELECTRICITY["accumulator"]["energy"], 3)),
            "prod": round(energy_produced, 3),
            "prod_units": ceil(
                round(energy_produced
                      / ELECTRICITY["accumulator"]["energy"], 3))
        }
    }


def output(power_calculation_result):
    print(
        f'Target power consumption:  '
        f'{power_calculation_result["power"]["facility"]} MW/s'
        )
    print(f'Powering:')
    print(
        f'  total:\t{power_calculation_result["power"]["total"]:5} MW/sec'
        f' ({power_calculation_result["power"]["units"]} solar panels)'
        )
    print(
        f'  facility:\t{power_calculation_result["power"]["facility"]:5}'
        f'MW/sec'
        )
    print(
        f'  storage:\t{power_calculation_result["power"]["storage"]:5} MW/sec'
        )
    print('Energy')
    print(
        f'  produced:\t{power_calculation_result["energy"]["prod"]} MJ'
        f' ({power_calculation_result["energy"]["prod_units"]} accumulators)'
        )
    print(
        f'  consumed:\t{power_calculation_result["energy"]["cons"]} MJ'
        f' ({power_calculation_result["energy"]["cons_units"]} accumulators)'
        )
    print()


# Constants
TICKS_PER_SECOND = 60
TOD = {
    "cycle": 25000,      # 100
    "midday": 12500,     # 50%
    "transition": 5000,  # 20%
    "night": 2500        # 10%
    }
ELECTRICITY = {
    "accumulator": {"power": 0.3, "energy": 5},
    "solar_panel": {"power": 0.06},  # 0.042 MW/sec avg
    "steam_engine": {"power": 0.9},
    "nuclear_reactor": {"power": 40.0},
    "electric_drill": {"power": 0.09},
    "electric_furnace": {"power": 0.18, "drain": 0.006},
    "pumpjack": {"power": 0.09},
    "pump": {"power": 0.03},
    "inserter_std": {"power": 0.0136, "drain": 0.0004},
    "inserter_lng": {"power": 0.02011, "drain": 0.0004},
    "inserter_fst": {"power": 0.0467, "drain": 0.0005},
    "inserter_flt": {"power": 0.0533, "drain": 0.0005},
    "inserter_pkt": {"power": 0.133, "drain": 0.001},
    "inserter_pkt_flt": {"power": 0.133, "drain": 0.001},
    "assembly_1": {"power": 0.0775, "drain": 0.0025},
    "assembly_2": {"power": 0.155, "drain": 0.005},
    "assembly_3": {"power": 0.388, "drain": 0.0125},
    "radar": {"power": 0.3},
    "lamp": {"power": 0.005}  # 0.0015 MW/sec avg, bc disabled during daytime
}


if __name__ == "__main__":
    clear()
    try:
        while True:
            intext = input("Facility power consumption, MW/sec: ")
            if intext.lower() in ["exit", "e", "quit", "q"]:
                quit()
            else:
                try:
                    clear()
                    result = power_calculation(
                        max(ELECTRICITY["solar_panel"]["power"],
                            float(intext))
                        )
                    output(result)

                except ValueError:
                    print("Value Error")

    except KeyboardInterrupt:
        # print('\r', end='')
        pass
