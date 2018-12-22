import time
import sys
import http.client
import collections

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

# # get the genres_id
# net = http.client.HTTPSConnection("api.themoviedb.org")
# net.request("GET", "/3/genre/movie/list?language=en-US&api_key=8b2060a1ce4ef3c46f793d841cf476bc", payload)
# genres= net.getresponse().read()
# print(genres)

# -----------------------------------------------Question 1.1.a---------------------------------------------

id_name_list=[]
api_key=sys.argv[1]
for page_num in range(1, 16):
    conn.request("GET", "/3/discover/movie?page="+str(page_num)+"&include_adult=false&include_video=false&sort_by="
                        "popularity.desc&primary_release_date.gte=2000-01-01&with_genres=35"
                        "&language=en-US&api_key="+api_key, payload)

    # &primary_release_date.lte="2000-01-01"
    # &with_genres=35

    res = conn.getresponse()
    data = res.read()

    string_data=str(data)
    list_index, idnum, name = 0, '', ''
    sign=['\'', ':', '\"']
    for i in range(len(string_data)-6):
        if string_data[i:i+4] == '"id"':
            k = i+4
            while string_data[k] != ',':
                if string_data[k].isdigit(): idnum += string_data[k]
                k += 1
        if string_data[i: i+7] == '"title"':
            k = i+7
            while string_data[k] != ',':
                if string_data[k] not in sign: name += string_data[k]
                k += 1
            id_name_list.append((idnum,name))
            idnum, name = '', ''
            list_index += 1

# print(id_name_list)
# print('\n'+str(len(id_name_list)))

# transfer the date into .csv file

with open("movie_ID_name.csv", 'w') as resultFile:
    for pair in id_name_list:
        resultFile.write(pair[0]+',"'+pair[1]+'"\n')


# ---------------------------------------------Question 1.1.c-------------------------------------------

similar_res_list=[]
meo = collections.defaultdict(int)
count=1
for pair in id_name_list:
    time.sleep(0.2)
    movie_id=pair[0]
    conn.request("GET", "/3/movie/"+movie_id+"/similar?page=1&language=en-US&api_key="+api_key, payload)

    similar_string = str(conn.getresponse().read())
    print("finding similarities for movie No."+str(count))
    # print(similar_string)
    sim_id, tag='', 0
    tmp_sim_id_store=[]
    for i in range(len(similar_string) - 6):
        if similar_string[i:i + 4] == '"id"':
            k = i + 4
            while similar_string[k] != ',':
                if similar_string[k].isdigit(): sim_id += similar_string[k]
                k += 1
            if tag<5:
                tag+=1
                target=movie_id+','+sim_id
                re_target=sim_id+','+movie_id
                if meo[target]<1 and meo[re_target]<1:
                    meo[target]+=1
                    similar_res_list.append(target)

                elif meo[target]<1 and meo[re_target]>=1 and int(movie_id)<int(sim_id):
                    meo[target]+=1
                    similar_res_list.remove(re_target)
                    similar_res_list.append(target)
                sim_id = ''
            else: break
    count+=1
    similar_res_list.extend(tmp_sim_id_store)

# print(similar_res_list)
# print('\n'+str(len(similar_res_list)))

with open("movie_ID_sim_movie_ID.csv", 'w') as resultFile:
    for pair in similar_res_list:
        # print(pair )
        resultFile.write(pair+'\n')
