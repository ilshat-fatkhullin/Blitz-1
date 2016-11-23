import pandas

STRUCTURE_FILE_NAME = 'course-217-structure.csv'
EVENTS_FILE_NAME = 'course-217-events.csv'

Events = pandas.read_csv(EVENTS_FILE_NAME)
Params = Events['action']
Events = Events.mask(Params == 'passed')
Events = Events.mask(Params == 'started_attempt')
Events.dropna(inplace=True)
Events = Events.sort_values(['user_id', 'time'])

EVENT_USER_ID = 0
EVENT_ACTION = 1
EVENT_STEP_ID = 2
EVENT_TIME = 3

Events.insert(4, 'module_position', 0)
Events.insert(5, 'lesson_position', 0)
Events.insert(6, 'step_position', 0)

EVENT_MODULE_POSITION = 4
EVENT_LESSON_POSITION = 5
EVENT_STEP_POSITION = 6

Structs = pandas.read_csv(STRUCTURE_FILE_NAME)

STRUCTURE_STEP_ID = 5
STRUCTURE_MODULE_POSITION = 2
STRUCTURE_LESSON_POSITION = 4
STRUCTURE_STEP_POSITION = 6

StructsDict = dict()

for row in Structs.values:
    StructsDict.update({row[STRUCTURE_STEP_ID]:[row[STRUCTURE_MODULE_POSITION], row[STRUCTURE_LESSON_POSITION], row[STRUCTURE_STEP_POSITION]]})

Values = Events.values
for i in range(len(Values)):
    Arr = StructsDict.get(Values[i][EVENT_STEP_ID])
    Values[i][EVENT_MODULE_POSITION] = Arr[0]
    Values[i][EVENT_LESSON_POSITION] = Arr[1]
    Values[i][EVENT_STEP_POSITION] = Arr[2]

Events = pandas.DataFrame(Values, columns=['user_id', 'action', 'step_id', 'time', 'module_position', 'lesson_position', 'step_position'])
Events = Events.sort_values(['user_id', 'module_position', 'lesson_position', 'step_position', 'time'])
print(Events.head(10))
Steps = []
for row in Structs.values:
    Steps.append([row[STRUCTURE_STEP_ID], 0])

Values = Events.values
LastTime = 0
LastUserId = 0
for i in range(1, len(Values)):
    if LastUserId != Values[i][EVENT_USER_ID]:
        LastTime = 0
        LastUserId = Values[i][EVENT_USER_ID]
    if Values[i - 1][EVENT_USER_ID] == Values[i][EVENT_USER_ID] and Values[i][EVENT_ACTION] == 'viewed' and Values[i - 1][EVENT_ACTION] == Values[i][EVENT_ACTION]:
        for j in range(len(Steps)):
            if Steps[j][0] == Values[i][EVENT_STEP_ID]:
                Steps[j][1]+=1
                break

Steps.sort(key=lambda x: x[1])
Steps.reverse()

for i in range(10):
    if i == 9:
        print(str(int(Steps[i][0])), end='')
    else:
        print(str(int(Steps[i][0])), end=',')