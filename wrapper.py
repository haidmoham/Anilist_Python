import json
import requests


import constants

def getTitleTypes():
    return {"english", "romaji", "native"}

def buildQuery(query, variables):
    json = {'query':query, 'variables':variables}
    return json

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

    response = requests.post(constants.getURL(), json=buildQuery(query, variables)) #{'query':query, 'variables':variables}
    json_obj = json.loads(response.content)

    # print(json.dumps(json_obj, indent=4, sort_keys=True))

    if (titleType in validTitles):
        return json_obj['data']['Media']['title'][titleType]
    else:
        return json_obj['data']['Media']['title']['english']

def getAnimeTitles(title="Naruto"):
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

    response = requests.post(constants.getURL(), json=buildQuery(query, variables))
    json_obj = json.loads(response.content)

    #print(json.dumps(json_obj, indent=4, sort_keys=4))

    return [json_obj['data']['Media']['title'][i] for i in titleTypes]
