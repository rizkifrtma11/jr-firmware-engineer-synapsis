def getStatistics(values):
    n = 0
    for _ in values:
        n += 1

    # value maksimum
    maksimum = values[0]
    for val in values:
        if val > maksimum:
            maksimum = val

    # value minimum
    minimum = values[0]
    for val in values:
        if val < minimum:
            minimum = val

    # value rata-rata
    total = 0
    for val in values:
        total += val
    mean = total / n

    # modus
    frequency = {}
    for val in values:
        if val in frequency:
            frequency[val] += 1
        else:
            frequency[val] = 1

    modus = values[0]
    max_count = frequency[modus]
    for key in frequency:
        if frequency[key] > max_count:
            modus = key
            max_count = frequency[key]

    # output
    print(f"Value : {values}")
    print(f"Nilai Maksimum : {maksimum}")
    print(f"Nilai Minimum : {minimum}")
    print(f"Nilai Rata-Rata : {mean}")
    print(f"Nilai Modbus : {modus}")


angka_list = [45, 30, 75, 45, 90, 60, 45, 80, 30, 90]
getStatistics(angka_list)
