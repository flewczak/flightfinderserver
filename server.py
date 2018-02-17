
import networkx as nx
import json
import os

from aiohttp import web
import socketio

import airlines_rating as airlines_rat
import airports_rating as airports_rat
import dictionary_air as dict_air
import routes_graph as rg
import rating_helper


airline_opinion_attributes = {'overall_rating', 'seat_comfort_rating', 'cabin_staff_rating', 'food_beverages_rating',
                              'inflight_entertainment_rating', 'ground_service_rating', 'wifi_connectivity_rating',
                              'value_money_rating', 'recommended'}
airport_opinion_attributes = {'overall_rating', 'queuing_rating', 'terminal_cleanliness_rating',
                              'terminal_seating_rating', 'terminal_signs_rating', 'food_beverages_rating',
                              'airport_shopping_rating', 'wifi_connectivity_rating', 'airport_staff_rating',
                              'recommended'}


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


sio = socketio.AsyncServer(async_mode='aiohttp', cors_credentials=True)
app = web.Application()
sio.attach(app)

G = nx.MultiDiGraph()
airlines_dict = dict_air.create_airlines_dict()
airport_dict = dict_air.create_airport_dict()

rg.add_nodes_to_graph(G)
rg.add_edges_to_graph(G)


@sio.on('connect', namespace='/main')
def connect(sid, environ):
    print("connected ", sid)


@sio.on('get_routes', namespace='/main')
async def get_routes(sid, data):
    print("route request: ", data)

    from_airport_number = data['from']
    to_airport_number = data['to']
    number_of_routes = data['number_of_routes'] - 1

    airline_opinion_weights = dict()
    airline_opinion_weights['overall_rating'] = 5
    airline_opinion_weights['seat_comfort_rating'] = data['airline']['seat_comfort_rating']
    airline_opinion_weights['cabin_staff_rating'] = data['airline']['cabin_staff_rating']
    airline_opinion_weights['food_beverages_rating'] = data['airline']['food_beverages_rating']
    airline_opinion_weights['inflight_entertainment_rating'] = data['airline']['inflight_entertainment_rating']
    airline_opinion_weights['ground_service_rating'] = data['airline']['ground_service_rating']
    airline_opinion_weights['wifi_connectivity_rating'] = data['airline']['wifi_connectivity_rating']
    airline_opinion_weights['value_money_rating'] = data['airline']['value_money_rating']
    airline_opinion_weights['recommended'] = data['airline']['recommended']

    airport_opinion_weights = dict()
    airport_opinion_weights['overall_rating'] = 5
    airport_opinion_weights['queuing_rating'] = data['airport']['queuing_rating']
    airport_opinion_weights['terminal_cleanliness_rating'] = data['airport']['terminal_cleanliness_rating']
    airport_opinion_weights['terminal_seating_rating'] = data['airport']['terminal_seating_rating']
    airport_opinion_weights['terminal_signs_rating'] = data['airport']['terminal_signs_rating']
    airport_opinion_weights['food_beverages_rating'] = data['airport']['food_beverages_rating']
    airport_opinion_weights['airport_shopping_rating'] = data['airport']['airport_shopping_rating']
    airport_opinion_weights['wifi_connectivity_rating'] = data['airport']['wifi_connectivity_rating']
    airport_opinion_weights['airport_staff_rating'] = data['airport']['airport_staff_rating']
    airport_opinion_weights['recommended'] = data['airport']['recommended']

    dictionary_airports_rating = dict()
    airports_rat.rating_airports(dictionary_airports_rating)
    dict_name_rat_name_route = rating_helper.rating_airlines_fix()
    rg.add_weight_to_all_node(G, dictionary_airports_rating, airport_opinion_weights, airport_dict,
                              dict_name_rat_name_route)

    dictionary_airlines_rating = dict()
    airlines_rat.rating_airlines(dictionary_airlines_rating)
    rg.add_weight_to_all_edge(G, dictionary_airlines_rating, airline_opinion_weights, airlines_dict)

    try:
        routes = rg.shortes_path_in_graph(G, from_airport_number, to_airport_number, number_of_routes)
        json_str = json.dumps(routes, default=dumper, indent=2)
        await sio.emit('routes_reply', {'flights': json_str, 'requestData': data}, namespace='/main', room=sid)
    except Exception as e:
        await sio.emit('error_reply', str(e), namespace='/main', room=sid)
        pass


if __name__ == '__main__':
    web.run_app(app, port=int(os.environ.get("PORT", 17995)))
