def rating_airlines_fix():
    out = dict()

    with open('data/airport_fix.txt', 'r', encoding="utf8") as file:
        for line in file:
            list_info = line.split(',')
            name_rating = list_info[2]
            name_route = list_info[3]
            name_route = name_route[0:len(list_info[3]) - 1]
            name_route = name_route.replace(" ", "-")
            name_route = name_route.lower()
            out[name_rating] = name_route
    return out


rating_airlines_fix()
