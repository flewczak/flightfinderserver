class AirLine:

    def __init__(self, airline_name, overall_rating, seat_comfort_rating, cabin_staff_rating, food_beverages_rating,
                 inflight_entertainment_rating, ground_service_rating, wifi_connectivity_rating, value_money_rating,
                 recommended):
        self.airline_name = airline_name
        self.overall_rating = overall_rating
        self.seat_comfort_rating = seat_comfort_rating
        self.cabin_staff_rating = cabin_staff_rating
        self.food_beverages_rating = food_beverages_rating
        self.inflight_entertainment_rating = inflight_entertainment_rating
        self.ground_service_rating = ground_service_rating
        self.wifi_connectivity_rating = wifi_connectivity_rating
        self.value_money_rating = value_money_rating
        self.recommended = recommended
        self.count = 0

    def add(self, overall_rating, seat_comfort_rating, cabin_staff_rating, food_beverages_rating,
            inflight_entertainment_rating, ground_service_rating, wifi_connectivity_rating, value_money_rating,
            recommended):
        self.overall_rating += overall_rating
        self.seat_comfort_rating += seat_comfort_rating
        self.cabin_staff_rating += cabin_staff_rating
        self.food_beverages_rating += food_beverages_rating
        self.inflight_entertainment_rating += inflight_entertainment_rating
        self.ground_service_rating += ground_service_rating
        self.wifi_connectivity_rating += wifi_connectivity_rating
        self.value_money_rating += value_money_rating
        self.recommended += recommended
        self.count += 1

    def add_list(self, list_of_param):
        self.overall_rating += list_of_param[0]
        self.seat_comfort_rating += list_of_param[1]
        self.cabin_staff_rating += list_of_param[2]
        self.food_beverages_rating += list_of_param[3]
        self.inflight_entertainment_rating += list_of_param[4]
        self.ground_service_rating += list_of_param[5]
        self.wifi_connectivity_rating += list_of_param[6]
        self.value_money_rating += list_of_param[7]
        self.recommended += list_of_param[8]
        self.count += 1

    def dict_airline_param(self):
        out = dict()
        out['overall_rating'] = self.overall_rating
        out['seat_comfort_rating'] = self.seat_comfort_rating
        out['cabin_staff_rating'] = self.cabin_staff_rating
        out['food_beverages_rating'] = self.food_beverages_rating
        out['inflight_entertainment_rating'] = self.inflight_entertainment_rating
        out['ground_service_rating'] = self.ground_service_rating
        out['wifi_connectivity_rating'] = self.wifi_connectivity_rating
        out['value_money_rating'] = self.value_money_rating
        out['recommended'] = self.recommended
        return out

    def __repr__(self):
        temp = self.recommended.__str__() + " " + self.count.__str__()
        return temp

    def average(self):
        self.overall_rating = self.overall_rating / self.count
        self.seat_comfort_rating = self.seat_comfort_rating / self.count
        self.cabin_staff_rating = self.cabin_staff_rating / self.count
        self.food_beverages_rating = self.food_beverages_rating / self.count
        self.inflight_entertainment_rating = self.inflight_entertainment_rating / self.count
        self.ground_service_rating = self.ground_service_rating / self.count
        self.wifi_connectivity_rating = self.wifi_connectivity_rating / self.count
        self.value_money_rating = self.value_money_rating / self.count
        self.recommended = self.recommended / self.count


def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False


# conversion str to int if not succeeded set default value 
def rating_fix(value, default_value=5.0):
    if not isfloat(value):
        return default_value
    else:
        return float(value)

#read opinions/rating about airlines from file
def rating_airlines(dictionary_airlines):
    with open('data/rating/airline.csv', 'r', encoding="utf8") as file:
        count = 1

        for line in file:
            if count != 1:
                list_info = line.split('","')
                # check if line load correctly else skip line 
                if len(list_info) == 20:
                    airline_name = (list_info[0])[1:len(list_info[0])]

                    tmp = list()
                    for i in range(11, 19):
                        tmp.append(rating_fix(list_info[i]))

                    recom_temp = (list_info[19])[0:len(list_info[19]) - 2]
                    tmp.append(rating_fix(recom_temp))

                    if airline_name in dictionary_airlines:
                        dictionary_airlines[airline_name].add_list(tmp)

                    else:
                        new_airline = AirLine(airline_name, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                        new_airline.add_list(tmp)
                        dictionary_airlines[airline_name] = new_airline

            count += 1

    # calculate average
    for i in dictionary_airlines.items():
        i[1].average()
