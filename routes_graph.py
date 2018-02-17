import networkx as nx

import geo_helper

# add nodes
def add_nodes_to_graph(G):
    with open('data/graph/airports.dat.txt', 'r', encoding="utf8") as file:
        count = 1
        for line in file:
            list_info = line.split(',')
            airport_id = list_info[0]
            airport_name = list_info[1]
            latitude = list_info[6]
            longitude = list_info[7]
            G.add_node(airport_id, weight=1, latitude=latitude, longitude=longitude)
            count += 1


# add edges
def add_edges_to_graph(G):
    with open('data/graph/routes.dat.txt', 'r', encoding="Latin-1") as file:
        for line in file:
            list_info = line.split(',')
            airline_id = list_info[1]
            source_airport_id = list_info[3]
            destination_airport_id = list_info[5]
            if source_airport_id != '\\N' and destination_airport_id != '\\N':
                if G.has_node(source_airport_id) == True and G.has_node(destination_airport_id) == True:
                    # tutaj dodawnie krwaedzi do grafu
                    G.add_edge(source_airport_id, destination_airport_id, weight=1, airline_id=airline_id)


# set weight of node
def add_weight_to_node(G, airport_id, weight):
    for i in G.nodes().data(data=True):
        if i[0] == airport_id:
            i[1]['weight'] = weight


# set weight of all the nodes based on opinions/rating
def add_weight_to_all_node(G, dict_airports_rating, dict_airport_param, dict_name_airport_id, dict_name_rat_name_route):
    count = 0
    count2 = 0
    for i in dict_airports_rating.items():
        weight_out = 0

        #calculate weight for specific airport
        for j in i[1].dict_airport_param().items():
            wght = dict_airport_param[j[0]]
            rat = j[1]
            weight_out += rat * wght

        weight_out = 1 / weight_out
        # multiplier to increase the weight value
        weight_out = weight_out * 100

        airport_id = dict_name_airport_id.get(dict_name_rat_name_route.get(i[0]))

        if airport_id is not None:
            count += 1
            G.node[airport_id]['weight'] = weight_out

        count2 += 1


# finding all the edges of the specific airline and seting weight + fix for distance
def add_weight_to_edge(G, airline_id, weight):
    for i in G.edges(data=True):
        if i[2]['airline_id'] == airline_id:
            lat1 = G.node[i[0]]['latitude']
            lon1 = G.node[i[0]]['longitude']
            lat2 = G.node[i[1]]['latitude']
            lon2 = G.node[i[1]]['longitude']
            # get weight of nodes to update weight of the edge - search for connection depends on rating of node 
            wght1 = G.node[i[0]]['weight']
            wght2 = G.node[i[1]]['weight']
            wght1 += 1
            wght2 += 1
            wght_node = wght1 * wght2
            #######
            dist = geo_helper.calc_distance(lat1, lon1, lat2, lon2)
            i[2]['weight'] = weight * dist.km * wght_node


# set weight for all the edges based on opinions/rating
def add_weight_to_all_edge(G, dict_airlines_rating, dict_airline_param, dict_name_airline_id):
    for i in dict_airlines_rating.items():
        weight_out = 0

        # calculate weight for specific airline 
        for j in i[1].dict_airline_param().items():
            wght = dict_airline_param[j[0]]
            rat = j[1]
            weight_out += rat * wght

        weight_out = 1 / weight_out
        airlines_id = dict_name_airline_id.get(i[0])
        # test if opinion refer to airline which is in file route.dat.txt 
        if airlines_id is not None:
            add_weight_to_edge(G, airlines_id, weight_out)


# find the shortest path
def shortes_path_in_graph(G, source_airport_id, destination_airport_id, k):
    # copy graph
    H = G.copy()
    airports_list = list()
    weigh_list = list()
    airline_list = list()
    for qq in range(0, k + 1):
        tmp = nx.single_source_dijkstra(H, source_airport_id, destination_airport_id, weight='weight')
        weigh_list.append(tmp[0])
        airports_list.append(tmp[1])
        airline_list_tmp = list()
        count = 0
        ptr = tmp[1]
        for i in tmp[1]:
            if count == 0:
                ptr = i
                count += 1
            else:
                wght = 99999999

                # find edge with the lowest weight that was used
                for (u, v, kk, c) in H.edges(data=True, keys=True):
                    ### c-dict data kk-key edges               
                    if u == ptr and v == i:
                        if (wght > c['weight']):
                            wght = c['weight']
                            kkey = kk
                            air_id = c['airline_id']
                airline_list_tmp.append(air_id)
                # go all the way and collect airlines numbers

                H.remove_edge(ptr, i, kkey)

                ptr = i

        airline_list.append(airline_list_tmp)

    print(weigh_list)
    print(airports_list)
    print(airline_list)

    return geo_helper.ShortestPaths(weigh_list, airports_list, airline_list)
