import webbrowser

import gmplot
import timeit
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from pyvis.network import Network

start = timeit.default_timer()

###################################################################################### 1.1 Get Locations and Plot Map #################################################################

#Geocoding coordinates for cities
geolocator = Nominatim(user_agent="geoapi")

kl = geolocator.geocode("Kuala Lumpur")
jakarta = geolocator.geocode("Jakarta")
bangkok = geolocator.geocode("Bangkok")
taipei = geolocator.geocode("Taipei")
hk = geolocator.geocode("Hong Kong")
tokyo = geolocator.geocode("Tokyo")
beijing = geolocator.geocode("Beijing")
seoul = geolocator.geocode("Seoul")

kl_coordinates = (kl.latitude, kl.longitude)
jakarta_coordinates = (jakarta.latitude, jakarta.longitude)
bangkok_coordinates = (bangkok.latitude, bangkok.longitude)
taipei_coordinates = (taipei.latitude, taipei.longitude)
hk_coordinates = (hk.latitude, hk.longitude)
tokyo_coordinates = (tokyo.latitude, tokyo.longitude)
beijing_coordinates = (beijing.latitude, beijing.longitude)
seoul_coordinates = (seoul.latitude, seoul.longitude)

#Initial map plotting
apikey=''
gmap = gmplot.GoogleMapPlotter(kl.latitude, kl.longitude, 4, apikey=apikey)
latitude = [kl.latitude, jakarta.latitude, bangkok.latitude, taipei.latitude, hk.latitude, tokyo.latitude, beijing.latitude, seoul.latitude]
longitude= [kl.longitude, jakarta.longitude, bangkok.longitude, taipei.longitude, hk.longitude, tokyo.longitude, beijing.longitude, seoul.longitude]
gmap.scatter(latitude, longitude, color='red', size=40, marker=True)
gmap.marker(kl.latitude,kl.longitude, color='white')
gmap.draw("Map.html")

new = 2
url = "Map.html"
webbrowser.open(url,new=new)


######################################################################################### 1.2 Get Distances ######################################################################

distances = [[0 for i in range(8)] for j in range(8)]
city_coordinates = [kl_coordinates, jakarta_coordinates, bangkok_coordinates, taipei_coordinates, hk_coordinates, tokyo_coordinates, beijing_coordinates, seoul_coordinates]

for i in range(8):
    for j in range(8):
        distances[i][j] = great_circle(city_coordinates[i], city_coordinates[j]).kilometers

net=Network("700px", "1000px")

net.add_node(0, label="Kuala Lumpur", size=10)
net.add_node(1, label="Jakarta", size=10)
net.add_node(2, label="Bangkok", size=10)
net.add_node(3, label="Taipei", size=10)
net.add_node(4, label="Hong Kong", size=10)
net.add_node(5, label="Tokyo", size=10)
net.add_node(6, label="Beijing", size=10)
net.add_node(7, label="Seoul", size=10)

for i in range(8):
    for j in range(8):
        if i is not j:
            value = str(round(great_circle(city_coordinates[i], city_coordinates[j]).kilometers, 2)) + " km"
            net.add_edge(i, j, label=value, font_color="white")

net.toggle_physics(True)
net.barnes_hut(spring_length=200)
net.show_buttons()
net.show("Travel Distances.html")

################################################################################## 1.3 Journey Planner ############################################################################


class Graph:
    # Constructor
    def __init__(self, edges, N):
        # A List of Lists to represent an adjacency list
        self.adjList = [[] for _ in range(N)]

        # add edges to the undirected graph
        for (src, dest) in edges:
            self.adjList[src].append(dest)
            self.adjList[dest].append(src)

hamiltonian_count= 0 #count for number of hamiltonian paths discovered
pathstring = [] #array to store all hamiltonian paths
unsorted_distance_array = [] #array to store path distances

#############################################################
#     Backtracking algorithm to find hamiltonian paths      #
#############################################################

def hamiltonian_path(g, v, visited, path, N, pathstring):
    if len(path) == N:
        # print hamiltonian path
        global hamiltonian_count
        hamiltonian_count+=1

        pathstring.append(path[:]) #append to global array
        print(path)

        return

    # Check if every edge starting from vertex v leads to a solution or not
    for w in g.adjList[v]:

        # process only unvisited vertices as hamiltonian
        # path visits each vertex exactly once
        if not visited[w]:
            visited[w] = True
            path.append(w)

            # check next vertex (w) to see if path is a valid hamiltonian
            hamiltonian_path(g, w, visited, path, N, pathstring)

            # Backtracking function
            visited[w] = False
            path.pop()

#Driver code for the backtracking algorithm
if __name__ == '__main__':
    #edgelist assignment
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
             (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
             (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
             (3, 4), (3, 5), (3, 6), (3, 7),
             (4, 5), (4, 6), (4, 7),
             (5, 6), (5, 7),
             (6, 7)]

    N = 8 #number of nodes

    g = Graph(edges, N) #create graph

    start = 0 #fixed starting node

    path = [start] #assigned a starting path

    # mark start node as visited
    visited = [False] * N
    visited[start] = True

    print("\nHamiltonian paths found:")
    hamiltonian_path(g, start, visited, path, N, pathstring)
    print("\nTotal hamiltonian paths: ", hamiltonian_count)

############################################################
#bubble-calc algorithm to calculate distances of all paths #
############################################################

def pathdistance(pathstring, city_coordinates, unsorted_distance_array):

    temp_distance = 0

    for i in range(len(pathstring)):
        current_path = pathstring[i]
        for j in range(7):
            temp_distance = round(great_circle(city_coordinates[current_path[j]], city_coordinates[current_path[j+1]]).kilometers + temp_distance, 2)

        unsorted_distance_array.append(temp_distance)
        temp_distance = 0

pathdistance(pathstring, city_coordinates, unsorted_distance_array)


###################################################
#      Timsort algorithm to sort path lengths     #
###################################################
minrun = 32

#Implementation of insertion sort
def InsSort(arr, start, end):
    for i in range(start + 1, end + 1):
        elem = arr[i]
        j = i - 1
        while j >= start and elem < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = elem
    return arr

#Implementation of merge sort
def merge(arr, start, mid, end):
    if mid == end:
        return arr
    first = arr[start:mid + 1]
    last = arr[mid + 1:end + 1]
    len1 = mid - start + 1
    len2 = end - mid
    ind1 = 0
    ind2 = 0
    ind = start

    while ind1 < len1 and ind2 < len2:
        if first[ind1] < last[ind2]:
            arr[ind] = first[ind1]
            ind1 += 1
        else:
            arr[ind] = last[ind2]
            ind2 += 1
        ind += 1

    while ind1 < len1:
        arr[ind] = first[ind1]
        ind1 += 1
        ind += 1

    while ind2 < len2:
        arr[ind] = last[ind2]
        ind2 += 1
        ind += 1

    return arr

# Actual Timsort implementation
def TimSort(arr):
    n = len(arr)

    for start in range(0, n, minrun):
        end = min(start + minrun - 1, n - 1)
        arr = InsSort(arr, start, end)

    curr_size = minrun
    while curr_size < n:
        for start in range(0, n, curr_size * 2):
            mid = min(n - 1, start + curr_size - 1)
            end = min(n - 1, mid + curr_size)
            arr = merge(arr, start, mid, end)
        curr_size *= 2
    return arr


# Driver code for the TimSort Algorithm
sorted_distance_array = unsorted_distance_array[:]

#Distance Array to be sorted
n = len(sorted_distance_array)

print("\nUnsorted path distances:\n", unsorted_distance_array)

TimSort(sorted_distance_array)
print("\nSorted path distances:\n", sorted_distance_array)

##############################################
#    Mini-Path-Mapper (MPM) algorithms       #
##############################################

shortest_path_array = [] #Important as the nodes for the shortest path are stored in order here
shortest_path_string= 'Kuala Lumpur > ' #solely for output purposes

for i in range(len(sorted_distance_array)):
    if unsorted_distance_array[i] == sorted_distance_array[0]:
        shortest_path_array = pathstring[i]

for i in range(1, 8):
    if shortest_path_array[i] == 1:
        shortest_path_string = shortest_path_string + 'Jakarta > '
    elif shortest_path_array[i]== 2:
        shortest_path_string = shortest_path_string + 'Bangkok > '
    elif shortest_path_array[i]== 3:
        shortest_path_string = shortest_path_string + 'Taipei > '
    elif shortest_path_array[i]== 4:
        shortest_path_string = shortest_path_string + 'Hong Kong > '
    elif shortest_path_array[i]== 5:
        shortest_path_string = shortest_path_string + 'Tokyo > '
    elif shortest_path_array[i]== 6:
        shortest_path_string = shortest_path_string + 'Beijing > '
    elif shortest_path_array[i]== 7:
        shortest_path_string = shortest_path_string + 'Seoul > '

print("\nThe shortest travel plan:\n", shortest_path_string)
print(" Total distance: ", sorted_distance_array[0], "km")


###################################################################################### 1.4 Plot Shortest Route #################################################################

#Another MPM algorithm just to plat the route

for i in range(8):
    if shortest_path_array[i] == 0:
        latitude[i] = kl.latitude
        longitude[i] = kl.longitude
    if shortest_path_array[i] == 1:
        latitude[i] = jakarta.latitude
        longitude[i] = jakarta.longitude
    if shortest_path_array[i] == 2:
        latitude[i] = bangkok.latitude
        longitude[i] = bangkok.longitude
    if shortest_path_array[i] == 3:
        latitude[i] = taipei.latitude
        longitude[i] = taipei.longitude
    if shortest_path_array[i] == 4:
        latitude[i] = hk.latitude
        longitude[i] = hk.longitude
    if shortest_path_array[i] == 5:
        latitude[i] = tokyo.latitude
        longitude[i] = tokyo.longitude
    if shortest_path_array[i] == 6:
        latitude[i] = beijing.latitude
        longitude[i] = beijing.longitude
    if shortest_path_array[i] == 7:
        latitude[i] = seoul.latitude
        longitude[i] = seoul.longitude


gmap.plot(latitude, longitude, 'blue', edge_width=4)
gmap.draw("Shortest Route.html")

new = 2
url2 = "Shortest Route.html"
webbrowser.open(url2,new=new)

###################################################################################### 2.5  #################################################################

import plotly.offline
import plotly.graph_objects as go
import timeit

# d is the number of characters in the input alphabet
d = 256


def search(pat, txt, q):
    M = len(pat)
    N = len(txt)
    pat = pat.replace(" ", "")
    p = 0  # hash value for pattern
    t = 0  # hash value for txt
    h = pow(d, M-1)

    result = False
    if M > N:
        return result
    else:
        # preprocessing
        for i in range(M):
            p = (d * p + ord(pat[i].lower())) % q
            t = (d * t + ord(txt[i].lower())) % q
        for s in range(N - M + 1):  # note the +1
            if p == t:  # check character by character
                match = True
                for i in range(M):
                    if pat[i].lower() != txt[s + i].lower():
                        match = False
                        break
                if match:
                    result = True
            if s < N - M:
                t = (t - h * ord(txt[s].lower())) % q  # remove letter s
                t = (t * d + ord(txt[s + M].lower())) % q  # add letter s+m
                t = (t + q) % q  # make sure that t >= 0
        return result


def rabin_karp_matcher(pattern, text):
    return search(pattern, text, 2207)


stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
             'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being',
             'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did',
             "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few',
             'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having',
             'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him',
             'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into',
             'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't",
             'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other',
             'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd",
             "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's",
             'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
             "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under',
             'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't",
             'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why',
             "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've",
             'your', 'yours', 'yourself', 'yourselves']



jakartaIO = open('News/jakarta.txt', 'r', encoding='utf-8-sig')
jakarta_text = jakartaIO.read().lower()
jakarta_text = jakarta_text.replace("\n", " ")
jakartaIO.close()

bangkokIO = open('News/bangkok.txt', 'r', encoding='utf-8-sig')
bangkok_text = bangkokIO.read().lower()
bangkok_text = bangkok_text.replace("\n", " ")
bangkokIO.close()

taipeiIO = open('News/taipei.txt', 'r', encoding='utf-8-sig')
taipei_text = taipeiIO.read().lower()
taipei_text = taipei_text.replace("\n", " ")
taipeiIO.close()

hongkongIO = open('News/hongkong.txt', 'r', encoding='utf-8-sig')
hongkong_text = hongkongIO.read().lower()
hongkong_text = hongkong_text.replace("\n", " ")
hongkongIO.close()

tokyoIO = open('News/tokyo.txt', 'r', encoding='utf-8-sig')
tokyo_text = tokyoIO.read().lower()
tokyo_text = tokyo_text.replace("\n", " ")
tokyoIO.close()

beijingIO = open('News/beijing.txt', 'r', encoding='utf-8-sig')
beijing_text = beijingIO.read().lower()
beijing_text = beijing_text.replace("\n", " ")
beijingIO.close()

seoulIO = open('News/seoul.txt', 'r', encoding='utf-8-sig')
seoul_text = seoulIO.read().lower()
seoul_text = seoul_text.replace("\n", " ")
seoulIO.close()


# get frequency of words in a text
def frequency(text, city):
    list_of_words = text.split()
    freq = {}
    for word in list_of_words:
        freq[word] = freq.get(word, 0) + 1
    keys = freq.keys()

    print("Frequencies of word for " + city + "'s article:\n\n" + str(freq) + "\n")


# print frequency of each word in text for every cities' article

frequency(jakarta_text, 'Jakarta')
frequency(bangkok_text, 'Bangkok')
frequency(taipei_text, 'Taipei')
frequency(hongkong_text, 'HongKong')
frequency(tokyo_text, 'Tokyo')
frequency(beijing_text, 'Beijing')
frequency(seoul_text, 'Seoul')

def word_count(text):
    stop_count = 0
    list_of_words = text.split()
    for word in stopwords:
        if rabin_karp_matcher(word, text):
            stop_count = stop_count + 1
            # delete stop words
            text = text.lower().replace(word, "", 1)

    return [stop_count, len(list_of_words,)]


jakarta_stop_count, jakarta_total_words = word_count(jakarta_text)
bangkok_stop_count, bangkok_total_words = word_count(bangkok_text)
taipei_stop_count, taipei_total_words = word_count(taipei_text)
hongkong_stop_count, hongkong_total_words = word_count(hongkong_text)
tokyo_stop_count, tokyo_total_words = word_count(tokyo_text)
beijing_stop_count, beijing_total_words = word_count(beijing_text)
seoul_stop_count, seoul_total_words = word_count(seoul_text)

#print(tokyo1_stop_count)
#print(tokyo1_total_words)
#print(tokyo1_text)



x = ["Jakarta", "bangkok","taipei","hongkong","Tokyo ","beijing","seoul"]
stop_counts = [ jakarta_stop_count,bangkok_stop_count,taipei_stop_count,hongkong_stop_count,tokyo_stop_count,beijing_stop_count,seoul_stop_count]
total_words = [ jakarta_total_words,bangkok_total_words,taipei_total_words,hongkong_total_words,tokyo_total_words,beijing_total_words,seoul_total_words]

data = [
    go.Histogram(
        histfunc="sum",
        y=stop_counts,
        x=x,
        name="Stop words"
    ),
    go.Histogram(
        histfunc="sum",
        y=total_words,
        x=x,
        name="Total words"
    )
]
layout = go.Layout(
    title=go.layout.Title(
        text="Stop Words & Total Words",
        xref='paper',
        x=0
    )
)
fig = go.Figure(data=data, layout=layout)
fig.show()




jakartaIO = open('News/jakarta.txt', 'r', encoding='utf-8-sig')
jakarta_text = jakartaIO.read().lower()

jakartaIO.close()

bangkokIO = open('News/bangkok.txt', 'r', encoding='utf-8-sig')
bangkok_text = bangkokIO.read().lower()

bangkokIO.close()

taipeiIO = open('News/taipei.txt', 'r', encoding='utf-8-sig')
taipei_text = taipeiIO.read().lower()

taipeiIO.close()

hongkongIO = open('News/hongkong.txt', 'r', encoding='utf-8-sig')
hongkong_text = hongkongIO.read().lower()

hongkongIO.close()

tokyoIO = open('News/tokyo.txt', 'r', encoding='utf-8-sig')
tokyo_text = tokyoIO.read().lower()

tokyoIO.close()

beijingIO = open('News/beijing.txt', 'r', encoding='utf-8-sig')
beijing_text = beijingIO.read().lower()

beijingIO.close()

seoulIO = open('News/seoul.txt', 'r', encoding='utf-8-sig')
seoul_text = seoulIO.read().lower()

seoulIO.close()


positive_word = open('Words/positivewords.txt', 'r', encoding='utf-8-sig')
positive_text = positive_word.read().lower().split('\n')

negative_word = open('Words/negativewords.txt', 'r', encoding='utf-8-sig')
negative_text = negative_word.read().lower().split('\n')


# getting the frequency of positive, negative and neutral words in a text
def wordcount(text):
    total_length = len(text.split())
    count = 0
    positive = 0
    negative = 0

    for pat in positive_text:
        pat = pat.replace(" ", "")
        if rabin_karp_matcher(pat, text):
            positive = positive + 1
            count = count + 1
    for pat in negative_text:
        pat = pat.replace(" ", "")
        if rabin_karp_matcher(pat, text):
            negative = negative + 1
            count = count + 1
    # neutral word is equal to the total words in text minus the total count
    # of words that is positive or negative
    neutral = total_length - count
    return positive, negative, neutral


# getting the no. of positive, negative and neutral words in the text
jakarta_pos, jakarta_neg, jakarta_neutral = wordcount(jakarta_text)
bangkok_pos, bangkok_neg, bangkok_neutral = wordcount(bangkok_text)
taipei_pos, taipei_neg, taipei_neutral = wordcount(taipei_text)
hongkong_pos, hongkong_neg, hongkong_neutral = wordcount(hongkong_text)
tokyo_pos, tokyo_neg, tokyo_neutral = wordcount(tokyo_text)
beijing_pos, beijing_neg, beijing_neutral = wordcount(beijing_text)
seoul_pos, seoul_neg, seoul_neutral = wordcount(seoul_text)


print("\nJakarta's article word count")
print("Positive word: " + str(jakarta_pos) + " word(s)")
print("Negative word: " + str(jakarta_neg) + " word(s)")
print("Neutral word: " + str(jakarta_neutral) + " word(s)")

print("\nBangkok's article word count")
print("Positive word: " + str(bangkok_pos) + " word(s)")
print("Negative word: " + str(bangkok_neg) + " word(s)")
print("Neutral word: " + str(bangkok_neutral) + " word(s)")

print("\nTaipei's article word count")
print("Positive word: " + str(taipei_pos) + " word(s)")
print("Negative word: " + str(taipei_neg) + " word(s)")
print("Neutral word: " + str(taipei_neutral) + " word(s)")

print("\nHong Kong's article word count")
print("Positive word: " + str(hongkong_pos) + " word(s)")
print("Negative word: " + str(hongkong_neg) + " word(s)")
print("Neutral word: " + str(hongkong_neutral) + " word(s)")

print("\nTokyo's article word count")
print("Positive word: " + str(tokyo_pos) + " word(s)")
print("Negative word: " + str(tokyo_neg) + " word(s)")
print("Neutral word: " + str(tokyo_neutral) + " word(s)")

print("\nBeijing's article word count")
print("Positive word: " + str(beijing_pos) + " word(s)")
print("Negative word: " + str(beijing_neg) + " word(s)")
print("Neutral word: " + str(beijing_neutral) + " word(s)")

print("\nSeoul's article word count")
print("Positive word: " + str(seoul_pos) + " word(s)")
print("Negative word: " + str(seoul_neg) + " word(s)")
print("Neutral word: " + str(seoul_neutral) + " word(s)")

################
#    Graph     #
################

x = ["Jakarta", "Bangkok", "Taipei", "Hong Kong", "Tokyo", "Beijing", "Seoul"]
positive_y = [jakarta_pos, bangkok_pos, taipei_pos, hongkong_pos, tokyo_pos, beijing_pos, seoul_pos]
negative_y = [jakarta_neg, bangkok_neg, taipei_neg, hongkong_neg, tokyo_neg, beijing_neg, seoul_neg]
neutral_y = [jakarta_neutral, bangkok_neutral, taipei_neutral, hongkong_neutral, tokyo_neutral,
             beijing_neutral, seoul_neutral]

data = [
    go.Histogram(
        histfunc="sum",
        y=positive_y,
        x=x,
        name="Positive words"
    ),
    go.Histogram(
        histfunc="sum",
        y=negative_y,
        x=x,
        name="Negative words"
    ),
    go.Histogram(
        histfunc="sum",
        y=neutral_y,
        x=x,
        name="Neutral words"
     )
]
layout = go.Layout(
    title=go.layout.Title(
        text="Positive, Negative & Neutral Words",
        xref='paper',
        x=0
    )
)
fig = go.Figure(data=data, layout=layout)
fig.show()
#  Sentiment & Conclusion  #
def sentiment(positive_frequency, negative_frequency, city):
    print("\n" + city.upper())
    if positive_frequency > negative_frequency:
        x = positive_frequency/negative_frequency
        print('The articles are giving positive sentiment')
        print('So the country has positive economic/financial situation of a ratio ')
        print(value(positive_frequency, negative_frequency))
    elif negative_frequency > positive_frequency:
        x = positive_frequency/negative_frequency
        print('The articles are giving negative sentiment')
        print('So the country has negative economic/financial situation of a ratio ')
        print(value(positive_frequency, negative_frequency))
    else:
        x = positive_frequency / negative_frequency
        print('The articles are giving neutral sentiment')
        print('So the country has neutral economic/financial situation of a ratio ')
        print(value(positive_frequency, negative_frequency))

def value(positive, negative):
    e = positive/negative
    return e

print("\n Concluding the cities' economic/fjnancial situation")
sentiment(jakarta_pos, jakarta_neg, "Jakarta")
sentiment(bangkok_pos, bangkok_neg, "Bangkok")
sentiment(taipei_pos, taipei_neg, "Taipei")
sentiment(hongkong_pos, hongkong_neg, "Hong Kong")
sentiment(tokyo_pos, tokyo_neg, "Tokyo")
sentiment(beijing_pos, beijing_neg, "Beijing")
sentiment(seoul_pos, seoul_neg, "Seoul")


jakartaValue= round(value(jakarta_pos, jakarta_neg),2)
bangkokValue= round(value(bangkok_pos, bangkok_neg),2)
taipeiValue= round(value(taipei_pos, taipei_neg),2)
hongkongValue= round(value(hongkong_pos, hongkong_neg),2)
tokyoValue= round(value(tokyo_pos, tokyo_neg),2)
beijingValue= round(value(beijing_pos, beijing_neg),2)
seoulValue= round(value(seoul_pos, seoul_neg),2)


data = [0, jakartaValue, bangkokValue,taipeiValue,hongkongValue,tokyoValue,beijingValue,seoulValue]
print(data)



##################################################################### 3.10 Find The Most Optimal Route Based on Sentiment #####################################################################
city = [kl_coordinates, jakarta_coordinates, bangkok_coordinates, hk_coordinates, taipei_coordinates, beijing_coordinates, seoul_coordinates, tokyo_coordinates]

optimal = ''
optimal_array = []

sentiment_arr = data[:]

#To Find the most optimal path as a baseline
def optimalPath():
    for i in range(1, 8):

        for j in range(i + 1, 8):

            if sentiment_arr[j] > sentiment_arr[i]:
                distance_ratio = (int(great_circle(city[j], city[i - 1]).kilometers) - int(
                    great_circle(city[i], city[i - 1]).kilometers)) / int(great_circle(city[i], city[i - 1]).kilometers)

                if distance_ratio < 0.4:
                    sentiment_ratio = (sentiment_arr[j] - sentiment_arr[i]) / sentiment_arr[i]

                    if sentiment_ratio > 0.02:

                        for k in range(i, j + 1):
                            temp = sentiment_arr[k]
                            sentiment_arr[k] = sentiment_arr[j]
                            sentiment_arr[j] = temp

optimalPath()
#Another MPM algorithm just to plat the route

for i in range(8):
    if sentiment_arr[i] == data[0]:
        optimal = optimal + "Kuala Lumpur > "
        optimal_array.append(0)
    if sentiment_arr[i] == data[1]:
        optimal = optimal + "Jakarta > "
        optimal_array.append(1)
    if sentiment_arr[i] == data[2]:
        optimal = optimal + "Bangkok > "
        optimal_array.append(2)
    if sentiment_arr[i] == data[3]:
        optimal = optimal + "Taipei > "
        optimal_array.append(3)
    if sentiment_arr[i] == data[4]:
        optimal = optimal + "Hong Kong > "
        optimal_array.append(4)
    if sentiment_arr[i] == data[5]:
        optimal = optimal + "Tokyo > "
        optimal_array.append(5)
    if sentiment_arr[i] == data[6]:
        optimal = optimal + "Beijing > "
        optimal_array.append(6)
    if sentiment_arr[i] == data[7]:
        optimal = optimal + "Seoul > "
        optimal_array.append(7)

print("\nMost optimal route based on distance and sentiment: \n",optimal)

count0 = 0
count0_array =[]
count1 = 0
count1_array =[]
count2 = 0
count2_array =[]
count3 = 0
count3_array =[]
count4 = 0
count4_array =[]
count5 = 0
count5_array =[]
count6 = 0
count6_array =[]
count7 = 0
count7_array =[]
count8 = 0
count8_array =[]

def arraySummary(summary):
    global optimal
    optimal = ''
    for i in range(8):
        if summary[i] == 0:
            optimal = optimal + "Kuala Lumpur > "
        if summary[i] == 1:
            optimal = optimal + "Jakarta > "
        if summary[i] == 2:
            optimal = optimal + "Bangkok > "
        if summary[i] == 3:
            optimal = optimal + "Taipei > "
        if summary[i] == 4:
            optimal = optimal + "Hong Kong > "
        if summary[i] == 5:
            optimal = optimal + "Tokyo > "
        if summary[i] == 6:
            optimal = optimal + "Beijing > "
        if summary[i] == 7:
            optimal = optimal + "Seoul > "
    print(optimal)

# Another MPM algorithm
for i in range(len(pathstring)):
    match_count = 0
    summary = pathstring[i]
    summary_distance = unsorted_distance_array[i]
    for j in range(8):
        if summary[j] == optimal_array[j]:
            match_count += 1
    if match_count == 0:
        count0 +=1
        count0_array.append(pathstring[i])
    if match_count == 1:
        count1 +=1
        count1_array.append(pathstring[i])
    if match_count == 2:
        count2 +=1
        count2_array.append(pathstring[i])
    if match_count == 3:
        count3 +=1
        count3_array.append(pathstring[i])
    if match_count == 4:
        count4 +=1
        count4_array.append(pathstring[i])
    if match_count == 5:
        count5 +=1
        count5_array.append(pathstring[i])
    if match_count == 6:
        count6 +=1
        count6_array.append(pathstring[i])
    if match_count == 7:
        count7 +=1
        count0_array.append(pathstring[i])
    if match_count ==8:
        count8 +=1
        count8_array.append(pathstring[i])

totalcount = count0+count1+count2+count3+count4+count5+count6+count7+count8
count0hist = count0/totalcount
count1hist = count1/totalcount
count2hist = count2/totalcount
count3hist = count3/totalcount
count4hist = count4/totalcount
count5hist = count5/totalcount
count6hist = count6/totalcount
count7hist = count7/totalcount
count8hist = count8/totalcount

Optimal_Route_Match = [count0hist, count1hist, count2hist, count3hist, count4hist, count5hist, count6hist,count7hist,count8hist]

x = ["0","1","2","3","4","5","6","7","8"]

data = [
    go.Bar(

        y=Optimal_Route_Match ,
        x=x,

    ),
]
layout = go.Layout(
    title=go.layout.Title(
        text="Probability Frequency Distribution",
        xref='paper',
        x=0
    )
)
fig = go.Figure(data=data, layout=layout)
fig.show()

print("\n##########################################################################")
print("In order of LEAST RECOMMENDED to MOST RECOMMENDED: ")
print("##########################################################################\n")

print("--------------------------------------------------------------------------")
print("Routes with 0 matches to optimal route NON EXISTENT")
print("--------------------------------------------------------------------------")
print()
print("--------------------------------------------------------------------------")
print("Routes with 1 matches to optimal route ( ABSOLUTELY NOT RECOMMENDED ) :")
print("--------------------------------------------------------------------------")
for i in range(len(count1_array)):
    arraySummary(count1_array[i])
print()
print("--------------------------------------------------------------------------")
print("Routes with 2 matches to optimal route ( NOT RECOMMENDED ) :")
print("--------------------------------------------------------------------------")
for i in range(len(count2_array)):
    arraySummary(count2_array[i])
print()
print("--------------------------------------------------------------------------")
print("Routes with 3 matches to optimal route ( NOT RECOMMENDED ) :")
print("--------------------------------------------------------------------------")
for i in range(len(count3_array)):
    arraySummary(count3_array[i])
print()
print("--------------------------------------------------------------------------")
print("Routes with 4 matches to optimal route ( AVERAGE ) :")
print("--------------------------------------------------------------------------")
for i in range(len(count4_array)):
    arraySummary(count4_array[i])
print()
print("--------------------------------------------------------------------------")
print("Routes with 5 matches to optimal route ( RECOMMENDED ) :")
print("--------------------------------------------------------------------------")
for i in range(len(count5_array)):
    arraySummary(count5_array[i])
print()
print("--------------------------------------------------------------------------")
print("Routes with 6 matches to optimal route ( HIGHLY RECOMMENDED ) :")
print("--------------------------------------------------------------------------")
for i in range(len(count6_array)):
    arraySummary(count6_array[i])
print()
print("--------------------------------------------------------------------------")
print("Routes with 7 matches with optimal route NON EXISTENT")
print("--------------------------------------------------------------------------")
print()
print("--------------------------------------------------------------------------")
print("Routes with COMPLETE MATCH with optimal route ( PERFECT MATCH - MOST OPTIMAL! ) :")
print("--------------------------------------------------------------------------")
for i in range(len(count8_array)):
    arraySummary(count8_array[i])
print()
print("#############################################################################")
print("Most optimal route based on distance and sentiment: ")
print()
print(optimal)
print("#############################################################################")


stop = timeit.default_timer()
print("\nTotal Runtime: ", stop-start)


