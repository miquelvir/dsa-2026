# Building Google Maps

`Data Structures and Algorithms - 2025 / 2026`

During this project, you will **build a program like Google Maps**. The user must be able to input a source address (`F`) and a destination addresses (`T`). Then, the program must print a list of directions guiding them from `F` to `T`. For example, if the user wants to go from `Passatge de la Dra. Remeis, 2` to `Avinguda Vertical, 4`, your program should print:

```
Route from Passatge de la Dra. Remeis, 2 (17.000000,30.666667) to Avinguda Vertical, 4 (12.333333,37.000000).

- Turn left in C. del Baixant
- Turn right in C. Pompeu Fabra
- Turn left in Av. Vertical
- You have reached your destination

The ETA is 3 minutes (600 meters).
```

<picture>
  <source 
    media="(prefers-color-scheme: dark)" 
    srcset="./problem_images/example_map_w_route_dark.svg">
  <source 
    media="(prefers-color-scheme: light)"
    srcset="./problem_images/example_map_w_route.svg">
  <img 
    alt="Example map with a route" 
    srcset="./problem_images/example_map_w_route.svg"
    style="display: block; margin: 0 auto; max-width: 600px; height: auto;">
</picture>

This lab is inspired by the [Google Maps (2019)](https://www.ijcaonline.org/archives/volume178/number8/mehta-2019-ijca-918791.pdf) paper.

# Deliverables

By the end of the project, every team must deliver:

- Source code for the program in your GitHub repository
- [A report](#report)

# Introduction to maps

Maps are composed of three components:
- Boxes wth the dashed outline represent **city blocks**. 
- City blocks are separated by **streets**. 
- An **intersection** is the place where two or more streets meet.

Maps contain two kinds of data: house numbers and streets. We have prepared different [maps datasets](#datasets) you can use for testing your program.

## House numbers

When describing the source (`F`) and destination (`T`) points in a map, we don't usually use coordinates. Instead, we use the street numbers of the houses in those streets. For example, `C. Pompeu Fabra, 9` is located in `C. Pompeu Fabra` between `C. del Baixant` and `Av. Vertical`.

<picture>
  <source 
    media="(prefers-color-scheme: dark)" 
    srcset="./problem_images/example_map_street_numbers_dark.svg">
  <source 
    media="(prefers-color-scheme: light)"
    srcset="./problem_images/example_map_street_numbers.svg">
  <img 
    alt="Example map with street numbers" 
    srcset="./problem_images/example_map_street_numbers.svg"
    style="display: block; margin: 0 auto; max-width: 600px; height: auto;">
</picture>

We store house numbers in `houses.txt` files. Each line represents a house. Each line contains the following information about the house separated by commas: `street_name`, `house_number`, `lat` and `lon`. For example:

```csv
C. del Baixant,1,11.000000,32.000000
C. del Baixant,3,11.666667,32.000000
C. del Baixant,5,12.333333,32.000000
C. del Baixant,2,11.000000,34.000000
C. del Baixant,4,11.666667,34.000000
C. del Baixant,6,12.333333,34.000000
C. del Baixant,8,15.000000,34.000000
C. del Baixant,10,16.000000,34.000000
C. del Baixant,12,17.000000,34.000000
```

The full file can be found in [./maps/xs_1/houses.txt](./maps/xs_1/houses.txt).

## Streets

We can give an ID to each intersection (red circle) to uniquely identify them. Then, each street (arrow) can be identified by the two intersections it joins. For example, `Ptge. de la Dra. Remeis` is known as `6-7`. When a street spans more than one block, it is divided in street segments. For example, `Av. Horitzontal` is known as `8-9`, `9-10` and `10-11`, depending on the concrete segment of the street.

<picture>
  <source 
    media="(prefers-color-scheme: dark)" 
    srcset="./problem_images/example_map_overlapped_graph_dark.svg">
  <source 
    media="(prefers-color-scheme: light)"
    srcset="./problem_images/example_map_overlapped_graph.svg">
  <img 
    alt="Example map with overlapped nodes (intersections) and edges (streets)" 
    srcset="./problem_images/example_map_overlapped_graph.svg"
    style="display: block; margin: 0 auto; max-width: 400px; height: auto;">
</picture>

Mathematically, we model the map as a directed graph. Each node in the graph is an intersection between one or more streets. Nodes are identified by their intersection ID. Each edge in the graph is a street. If an edge is bi-directional, it represents a two-way street (e.g. both `9-10` and `10-9`); otherwise, it represents a one-way street.

<picture>
  <source 
    media="(prefers-color-scheme: dark)" 
    srcset="./problem_images/example_map_graph_dark.svg">
  <source 
    media="(prefers-color-scheme: light)"
    srcset="./problem_images/example_map_graph.svg">
  <img 
    alt="Example map as a graph" 
    srcset="./problem_images/example_map_graph.svg"
    style="display: block; margin: 0 auto; max-width: 250px; height: auto;">
</picture>

We store streets in `streets.txt` files. Each line represents a street. Two-way streets are represented as two lines, one for each direction. Each line contains the following information about the street separated by commas: `from_intersaction_id`, `from_intersection_lat`, `from_intersection_lon`, `to_intersection_id`,  `to_intersection_lat`, `to_intersection_lon`, `length_meters`, `street_name`. For example:

```csv
1,10.000000,33.333333,4,13.333333,33.333333,100,C. del Baixant
3,13.333333,30.000000,4,13.333333,33.333333,100,C. Pompeu Fabra
4,13.333333,33.333333,5,13.333333,36.666667,100,C. Pompeu Fabra
5,13.333333,36.666667,2,10.000000,36.666667,100,Av. Vertical
6,16.666667,30.000000,7,16.666667,33.333333,100,Ptge. de la Dra. Remeis
7,16.666667,33.333333,4,13.333333,33.333333,50,C. del Baixant
8,20.000000,30.000000,9,20.000000,33.333333,100,Av. Horitzontal
9,20.000000,33.333333,8,20.000000,30.000000,100,Av. Horitzontal
7,16.666667,33.333333,9,20.000000,33.333333,50,C. del Baixant
9,20.000000,33.333333,10,20.000000,36.666667,100,Av. Horitzontal
10,20.000000,36.666667,9,20.000000,33.333333,100,Av. Horitzontal
10,20.000000,36.666667,11,20.000000,40.000000,100,Av. Horitzontal
11,20.000000,40.000000,10,20.000000,36.666667,100,Av. Horitzontal
```

The full file can be found in [./maps/xs_1/streets.txt](./maps/xs_1/streets.txt).

# Work breakdown

We have divided all tasks into four categories so you can prioritize implementing them accordingly.

| Weight               | Description                              | Symbol   |
|----------------------|------------------------------------------|----------|
| 60% | Essential, needed to get something working       | (^)      |
| 20% | Nice-to-haves, not required to get something working | (^^)     |
| 10% | Difficult, complex exercises             | (^^^)    |
| 10% | Advanced, challenges for diving deep       | (^^^^)   |


## Lab 0: Developer Setup

Start setting up before the session:
- Create the repository from the [template](https://github.com/new?template_name=dsa-2026&template_owner=miquelvir) using name `dsa-2026-p000-00`. For example, if you are group `2` in lab `102`, use this name: `dsa-2026-p102-2`.
- [Share the repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository) with your group.
- [Share the repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository) with all teacher assistants and professors: 
  - [@miquelvir](https://github.com/miquelvir)
  - [@hectorflorido](https://github.com/hectorflorido)
  - [@psantosUPF](https://github.com/psantosUPF)
  - [@mcalveraupf](https://github.com/mcalveraupf)
  - [@spapadiamantis](https://github.com/spapadiamantis)
  - [@ludthor](https://github.com/ludthor)
  - [@Mohamed0Taha](https://github.com/Mohamed0Taha)
- Complete the [developer setup](./DEVELOPER_SETUP.md) guide.

## Lab 1: Finding the coordinates of an address

After this lab session, your program should:
- Ask the user for a map (`xs_1`, `xs_2`, `md_1`, `lg_1` or `xl_1`). (^)
- Ask the user for a street name and house number (e.g. `Carrer de Roc Boronat, 138`). Print its coordinates. (^)
- Print its coordinates. (^)

To do so, you will need to implement:
- Reading and parsing `houses.txt` files (^)
- Storing houses in a house linked list (^)
- Sequential search amongst the houses linked list (^)
- Find streets even if casing does not match (e.g. `Carrer de roc boronat` instead of `Carrer de Roc Boronat`) or using abbreviations (e.g. `C. de Roc Boronat` instead of `Carrer de Roc Boronat`). (^^)
- If the user writes a known street but an invalid number, print the valid street numbers in the street. If the user writes a street which is not known (e.g. `Carrer de Roc Voronat` instead of `Carrer de Roc Boronat`), print the most similar streets and their numbers. To do so, calculate the [Levenshtein distance](#levenshtein-distance) with all streets and print all streets with a Levenshtein distance below 3. (^^^)

## Lab 2: Finding the coordinates of a place

After this lab session, your program should:
- Allow the user to pick between an address, coordinate or a place. If the user picks a place, ask the user for the name of a place (e.g. `Àrea Tallers`). Print its coordinates. (^^)

To do so, you will need to implement:
- Reading and parsing `places.txt` files (^^)
- Storing places in a place linked list (^^)
- Sequential search amongst the places linked list (^^)
- If the user writes a place which is not known (e.g. `Area Tallers` instead of `Àrea Tallers`), print the most similar places. To do so, calculate the [Levenshtein distance](#levenshtein-distance) with all places and print all places less than 3 edits away. (^^^)

## Lab 3: Finding the closest street segment

After this lab session, your program should:
- Print between which two intersections is that street number located. (^)

To do so, you will need to implement:
- Reading and parsing `streets.txt` files (^)
- Storing all street segments in a linked list (^)
- Compute the distance between the user position and every street to find the closest one. You need to calculate the [midpoint of every street segment](#midpoint-between-coordinates) and use the [Haversine formula](#haversine-formula) to compute the distance between the user coordinates and each street midpoint. (^)
- Print which streets are connected to this one. E.g. to which streets can the user immediately go from his position. (^)

## Lab 4: Finding connected streets efficiently

To do so, you will need to implement:
- Load all streets from the list into an intersection hashmap, with the key being the intersection id and the value being a list of street segments it is connected to. (^)
- A hash map (^)

> [!NOTE]
> Don't remove the old version finding connected streets from the list. You will need it to compare Lab 3 and Lab 4 for the report.

## Lab 5: The path between two positions

After this lab session, your program should:
- Ask the user for a destination (coordinates, place or address like the source). (^)
- Print the step by step directions. (^)

To do so, you will need to implement:
- Breadth first search in a graph (^)
- A queue (^)

## Lab 6 & 7: Make it your own

Use these two sessions to finish work from previous labs. Once you are done, implement some of the suggested difficult challenges or some suggested by you.

## Lab 8 & 9: Interviews

During the last two lab sessions, you need to defend your project during the interviews with your Teacher Assistant or Professor.

# Datasets

The repository contains different maps you can use to test your program inside the [maps](./maps/) folder. Start testing with `xs_1` (the smallest and simplest map). Then progress towards bigger and more complex maps like `md_1`, or `lg_1`.

## xs_1

A small synthetic map with 11 intersections.

<picture>
  <source 
    media="(prefers-color-scheme: dark)" 
    srcset="./problem_images/example_map_dark.svg">
  <source 
    media="(prefers-color-scheme: light)"
    srcset="./problem_images/example_map.svg">
  <img 
    alt="xs1 map" 
    srcset="./problem_images/example_map.svg"
    style="display: block; margin: 0 auto; max-width: 300px; height: auto;">
</picture>

[View files.](./maps/xs_1/)

## xs_2

A small real map of a couple of city blocks around the University with 71 intersections.

![map](./problem_images/xs_2_map.png)

[View in OpenStreetMap.](https://www.openstreetmap.org/export#map=18/41.403585/2.194433)

[View files.](./maps/xs_2/)

## md_1

A medium real map of the city blocks around the University with 1122 intersections.

![map](./problem_images/md_1_map.png)

[View in OpenStreetMap.](https://www.openstreetmap.org/export#map=16/41.40354/2.19729)

[View files.](./maps/md_1/)

## lg_1

A large real map of Poblenou with 3283 intersections.

![map](./problem_images/lg_1_map.png)

[View in OpenStreetMap.](https://www.openstreetmap.org/export#map=15/41.39820/2.19744)

[View files.](./maps/lg_1/)

## xl_1

An extra large real map of Barcelona with 15378 intersections.

![map](./problem_images/xl_1_map.png)

[View in OpenStreetMap.](https://www.openstreetmap.org/export#map=14/41.39532/2.16680)

[View files.](./maps/xl_1/)

# Report

TODO

# Reference

## Levenshtein Distance

This algorithm computes how many edits there are between two strings `a` and `b`. The higher the number, the more different `a` and `b` are. The lower the number, the more similar `a` and `b` are.

If two strings have a low Levensthein Distance, it is probably that `a` is a version with typos of `b` (the correct string).

```c
function LevenshteinDistance(a, b):
    m ← length(a)
    n ← length(b)

    create matrix D of size (m+1) × (n+1)

    for i from 0 to m:
        D[i][0] ← i

    for j from 0 to n:
        D[0][j] ← j

    for i from 1 to m:
        for j from 1 to n:
            if a[i-1] = b[j-1]:
                cost ← 0
            else:
                cost ← 1

            D[i][j] ← minimum(
                D[i-1][j] + 1,      // deletion
                D[i][j-1] + 1,      // insertion
                D[i-1][j-1] + cost  // substitution
            )

    return D[m][n]
```

## Haversine formula

This formula allows approximately calculating the distance between any two coordinates.

```c
typedef struct position {
  double lat;
  double lon;
} Position;

double toRadians(double degree) {
    return degree * (M_PI / 180.0);
}

double haversine(Position posA, Position posB) {
    double lat1 = toRadians(posA.lat);
    double lon1 = toRadians(posA.lon);
    double lat2 = toRadians(posB.lat);
    double lon2 = toRadians(posB.lon);

    double dLat = lat2 - lat1;
    double dLon = lon2 - lon1;
    double a = pow(sin(dLat / 2), 2) +
    cos(lat1) * cos(lat2) * pow(sin(dLon / 2), 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    return EARTH_RADIUS * c;
}
```


## Midpoint between coordinates

You need to compute the distance between the user position and each street to decide which street is the user closest to. I.e. many user positions will be close to `3` or `4`, but only positions close to both `3` and `4` are located in the `3-4` segment. The easiest way is to calculate the midpoint coordinate, and then check the distance between the user position and the midpoint.

<picture>
  <source 
    media="(prefers-color-scheme: dark)" 
    srcset="./problem_images/example_map_midpoint_dark.svg">
  <source 
    media="(prefers-color-scheme: light)"
    srcset="./problem_images/example_map_midpoint.svg">
  <img 
    alt="xs1 map" 
    srcset="./problem_images/example_map_midpoint.svg"
    style="display: block; margin: 0 auto; max-width: 300px; height: auto;">
</picture>


This formula allows calculating the coordinate in the midpoint of two other coordinates.

```c
typedef struct position {
  double lat;
  double lon;
} Position;

double toDegrees(double radians) {
    return radians * (180.0 / M_PI);
}

double toRadians(double degree) {
    return degree * (M_PI / 180.0);
}

Position midpoint(Position a, Position b) {
    double lat1 = toRadians(a.lat);
    double lon1 = toRadians(a.lon);
    double lat2 = toRadians(b.lat);
    double lon2 = toRadians(b.lon);

    double x1 = cos(lat1) * cos(lon1);
    double y1 = cos(lat1) * sin(lon1);
    double z1 = sin(lat1);

    double x2 = cos(lat2) * cos(lon2);
    double y2 = cos(lat2) * sin(lon2);
    double z2 = sin(lat2);

    double x = (x1 + x2) / 2.0;
    double y = (y1 + y2) / 2.0;
    double z = (z1 + z2) / 2.0;

    double lon = atan2(y, x);
    double hyp = sqrt(x * x + y * y);
    double lat = atan2(z, hyp);

    Position mid;
    mid.lat = toDegrees(lat);
    mid.lon = toDegrees(lon);
    return mid;
}
```

## Breadth First Search

You can use Breadth First Search (BFS) to find a path between two intersections in the street graph.

```
BFS(intersections_graph, fromStreet, toStreet):
    create an empty queue of street lists, Q

    create a street list [fromStreet], initial_path
    enqueue initial_path into Q
    create a street list [], visited

    while Q is not empty:
        path = dequeue(Q)
        current_street = path[-1]

        if current_street == toStreet:
            return path
        
        if current_street not in visited:
            add current_street to visited

            for connected_street in intersections_graph[current_street.to_intersection_id]:
                if connected_street not in visited:
                    new_path = path + [connected_street]
                    enqueue new_path into Q

    return NULL   # no path found
```

# FAQ 

## How can I know where a given coordinate is?

You can copy any coordinate into [Google Maps](https://www.google.es/maps) to find it. For example, if you look for `41.403585699999994,2.1940067`, you will find [our university](https://www.google.es/maps/place/41%C2%B024'12.9%22N+2%C2%B011'38.4%22E/@41.4035857,2.1930963,803m/data=!3m2!1e3!4b1!4m4!3m3!8m2!3d41.4035857!4d2.1940067?entry=ttu&g_ep=EgoyMDI1MTAyOS4yIKXMDSoASAFQAw%3D%3D).

## How can I create a custom map?

See the [maps builder](./../maps_builder/README.md).