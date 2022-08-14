import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    #dummypath(source, target)
    shortest_path(source, target)
    
    """
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
    """
def dummypath(source, target):
    start = Node(state=source, parent=None,action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    action = people[frontier.frontier[0].state]['movies']
    mystars = []
    explored = []
    num_explored = -1
    heck_yea = True
    while heck_yea:
        node = frontier.remove()
        print('---------------------------------')
        print('my guy is now: ',people[node.state]['name'])
        for h in frontier.frontier:
            print('next person: ',people[h.state]['name'])

        print('---------------------------------')
        
        num_explored += 1
        explored.append(node)
        #checkin if we have arrived
        
        if node.state == target:
            print('num explored: ',num_explored)
            print('we have arrived')
            print('path:')
            for c in explored:
                #print(c.state,'',movies[c.action]['title'])
                print(people[c.state]['name'])
                print(c.action)
            heck_yea = False
            #to be continued

        action = people[node.state]['movies']
        
        #adding new people
        for i in action:
            for x in movies[i]['stars']:
                mystars.append(x)
                child = Node(state=x,parent=start, action=i)
                for m in explored:
                    if x != m.state:
                        print('hi ', m.state)
                        frontier.add(child)
                    elif x == m.state:
                        if x == node.state:
                            frontier.add(child)
                        print('hi2 ', m.state)
                        frontier.frontier.remove(child)

        if len(frontier.frontier) == 0:
            print('Those people are not linked!')
            heck_yea = False
        
    

def find_path(mylist):
    thepath = []
    last_item = mylist[-1]
    def printit(variable):
        if variable.parent == None:
            thepath.append(variable)
            return thepath
        thepath.append(variable)
        return printit(variable.parent)
    printit(last_item)

    return thepath
     

    
def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    start = Node(state=source, parent=None,action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    explored = []
    explored_obj = []
    num_explored = -1
    mainloop = True

    while mainloop:
        #bfs
        node = frontier.remove()
        explored.append(node.state)
        explored_obj.append(node)
        num_explored += 1

        #checking if we reached the goal state
        if node.state == target:
            for mynode in explored_obj:
                if mynode.parent != None:
                    print('from {} to {} by movie {}'.format(people[mynode.parent.state]['name'],people[mynode.state]['name'],movies[mynode.action]['title']))
            print('Steps: {}'.format(num_explored))
            ft = find_path(explored_obj)
            ft.reverse()
            for i in ft:
                print(people[i.state]['name'])
            
            mainloop = False

        nb = neighbors_for_person(node.state)
        
        #adding neighbors to the frontier
        for action, state in nb:
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)
        
        #checking if there any state left in the frontier
        if len(frontier.frontier) == 0:
            for mynode in explored_obj:
                if mynode.parent != None:
                    print('from {} to {} by movie {}'.format(people[mynode.parent.state]['name'],people[mynode.state]['name'],movies[mynode.action]['title']))
            print('Steps: {}'.format(num_explored))
            mainloop == False


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
