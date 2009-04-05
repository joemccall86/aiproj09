from direct.task import Task

def taskTimer(task):
    taskTimer.elapsedTime = task.time - taskTimer.previousTime
    taskTimer.previousTime = task.time
    return Task.cont
    
taskTimer.previousTime = 0
taskTimer.elapsedTime = 0
