def create_airlines_dict():
    with open('data/graph/airlines.dat.txt', 'r', encoding="utf8") as file:
        dictionary_airlines = dict()
        for line in file:
            list_info = line.split(',')
            airline_id = list_info[0]
            airline_name = list_info[1]

            airline_name = airline_name.lower()
            airline_name = airline_name.replace(" ", "-")
            airline_name = airline_name.replace("\"", "")
            dictionary_airlines[airline_name] = airline_id

        return dictionary_airlines


def create_airport_dict():
    with open('data/graph/airports.dat.txt', 'r', encoding="utf8") as file:
        dictionary_airport = dict()
        for line in file:
            list_info = line.split(',')
            airport_id = list_info[0]
            airport_name = list_info[1]

            airport_name = airport_name.lower()
            airport_name = airport_name.replace(" ", "-")
            airport_name = airport_name.replace("\"", "")
            dictionary_airport[airport_name] = airport_id
        return dictionary_airport
