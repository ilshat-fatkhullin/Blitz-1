import pandas

STRUCTURE_FILE_NAME = 'course-217-structure.csv'
EVENTS_FILE_NAME = 'course-217-events.csv'

Events = pandas.read_csv(EVENTS_FILE_NAME)

Structs = pandas.read_csv(STRUCTURE_FILE_NAME)
Params = Structs['step_cost']
Structs = Structs.where(Params > 0)
Structs.dropna(inplace=True)
Params = Events['action']
Events = Events.mask(Params == 'viewed')
Events = Events.mask(Params == 'started_attempt')
Events.dropna(inplace=True)
FormattedEvents = Events.sort_values(['user_id', 'time'])

Users = []

def GetCost(stepId):
    for s in Structs.values:
        if s[5] == stepId:
            return 1
    return 0

LastUserId = -1
CostSum = 0
StartTime = 0
for Event in FormattedEvents.values:
    if Event[0] != LastUserId:
        LastUserId = Event[0]
        CostSum = 0
        StartTime = 0
    if Event[1] == 'discovered':
        if StartTime == 0:
            StartTime = Event[3]
    else:
        Cost = GetCost(Event[2])
        CostSum+=Cost
        if CostSum == 24 and Cost != 0:
            Users.append([LastUserId, Event[3] - StartTime])

Users.sort(key=lambda x: x[1])
i = 0
for i in range(10):
    if i == 9:
        print(str(int(Users[i][0])), end='')
    else:
        print(str(int(Users[i][0])), end=',')