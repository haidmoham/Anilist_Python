import json
import requests


import constants

def getTitleTypes():
    return {"english", "romaji", "native"}

def buildQuery(query, variables):
    response = requests.post(constants.getURL(), json={'query':query, 'variables':variables})
    json_obj = json.loads(response.content)
    return json_obj

def printJsonObj(json_obj):
    print(json.dumps(json_obj, indent=4, sort_keys=True))

def getTitleByID(titleType="english", id=1):
    validTitles = getTitleTypes()

    query = """
        query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title {
            romaji
            english
            native
            }
        }
        }
    """
    variables = {
        'id': max(1, id)
    }

    json_obj = buildQuery(query, variables)
    #printJsonObj(json_obj)

    if (titleType in validTitles):
        return json_obj['data']['Media']['title'][titleType]
    else:
        return json_obj['data']['Media']['title']['english']



def getAnimeTitles(title="Cowboy Bebop"):
    titleTypes = getTitleTypes()
    query = """
    query ($title: String) {
    Media (search: $title, type:ANIME) {
        title {
        romaji
        english
        native
        }
    }
    }
    """
    variables = {
        'title': title
    }

    json_obj = buildQuery(query, variables)
    #printJsonObj(json_obj)

    return [json_obj['data']['Media']['title'][i] for i in titleTypes]

"""Return the current release status of an anime (default) or manga. 

"""
def getStatus(title="Cowboy Bebop", type="ANIME"):
    query = """
    query ($title: String) {
    Media (search: $title, type:ANIME) {
        status
    }
    }
    """
    variables = {
        'type': type
    }

    json_obj = buildQuery(query, variables)
    #printJsonObj(json_obj)

    return json_obj['data']['Media']['status']

def getDates(title="Cowboy Bebop"):
    query = """
    query ($title: String) {
    Media (search: $title, type:ANIME) {
        startDate {
            year
            month
            day
        }
        endDate {
            year
            month
            day
        }
    }
    }
    """
    variables = {
        'title': title
    }
    json_obj = buildQuery(query, variables)
    
    dateList = []
    dateList.append(json_obj['data']['Media']['startDate'])
    dateList.append(json_obj['data']['Media']['endDate'])

    return dateList

def getSeasonYear(title="Cowboy Bebop"):
    query = """
    query ($title: String) {
    Media (search: $title, type:ANIME) {
            season
            startDate {
                year
        }
    }
    }
    """
    variables = {
        'title': title
    }
    json_obj = buildQuery(query, variables)
    
    stringOut = str(json_obj['data']['Media']['season']).capitalize() + " " + str(json_obj['data']['Media']['startDate']['year'])

    return stringOut

# print(getDates("Violet Evergarden"))
print(getSeasonYear("Violet Evergarden"))