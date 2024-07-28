input_vals = [
    [
        True,       # state -> to | True
        True,       # event -> True
        50,         # num state -> number
        "added",    # pers. notification -> update type
        10,         # num event -> number
        True,       # mqtt -> True
        True,       # zone -> True
        True,       # calendar -> True
        True,       # template -> True
        True,       # zone -> True
        True,       # state, to: limited template -> True
        "turned_off",   # device -> type
        "20",       # state -> to | True
        True,       # home assistant -> True
        True,       # tag -> True
        True,       # sun -> True
        True,       # time -> True
        True,       # time_pattern-> True
        True,       # webhook -> True
        True,       # conversation -> True
    ],
]

triggered = False
trigger_id = None
trigger = input_vals[0]

if (
    trigger[0]
    or trigger[1]
    or (10 < trigger[2] < 50000)
    or (trigger[3] == "added" or trigger[3] == "removed")
    or (2 < trigger[4] < 4000)
    or trigger[5]
    or (trigger[6] == "person.admin")
    or trigger[7]
    or trigger[8]
    or trigger[9]
    or trigger[10]
):
    triggered = True

if triggered:
    print("Triggered")
