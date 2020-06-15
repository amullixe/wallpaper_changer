import datetime
import win32com.client
import pywintypes

class Task_scheduler():
    # TYPES: action_id(str), action_path(str), action_work_dir(str),
    #  action_args(str), time_btw_task_repetitions(int) description(str)
    def __init__(self, params=None):
        if params:
            self.init_params(params)
        self.task_name = "WallpaperChangerTask"

        # init scheduler
        self.scheduler = win32com.client.Dispatch('Schedule.Service')
        self.scheduler.Connect()
        self.root_folder = self.scheduler.GetFolder('\\')

    def init_params(self, params):
        self.action_id = params['action_id']
        self.action_path = params['action_path']
        self.action_work_dir = params['action_work_dir']
        self.action_args = params['action_args']
        self.time_btw_task_repetitions = params['time_btw_task_repetitions']
        self.description = params['description']

    def print_not_enough_rights(self):
        print('Not enough rights.')

    def is_there_such_task(self, task_name):
        tasks = list(self.root_folder.GetTasks(0))

        for task in tasks:
            if task.name == task_name:
                print(task.Path)
                return True
        return False

    def delete_task(self):
        is_task_name_in_tasks = self.is_there_such_task(self.task_name)
        if is_task_name_in_tasks:
            # delete task
            try:
                self.root_folder.DeleteTask(self.task_name, 0)
                return True
            except pywintypes.com_error:
                print_not_enough_rights()
                return False
    
    def set_time_designator(self, time):
        # if last char in time is 'H' or 'M' then
        if time[-1] != 'D':
            return 'T'
        else:
            return ''

    # Examples: 10D, 5M, 50H
    def get_mins_from_utc(self, time_str):
        if time_str[-1] == 'H':
            return int(time_str[:-1])*60
        elif time_str[-1] == 'D':
            return int(time_str[:-1])*60*24
        else:
            return int(time_str[:-1])

    def create_task(self):
        task_def = self.scheduler.NewTask(0)

        # get mins before first start the program
        first_start_mins = self.get_mins_from_utc(self.time_btw_task_repetitions)
        # Create trigger
        start_time = datetime.datetime.now() + datetime.timedelta(minutes=first_start_mins)
        
        TASK_TRIGGER_TIME = 1
        trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
        trigger.StartBoundary = start_time.isoformat()
        # set repetition pattern - every day 1 time
        
        repetition_pattern = trigger.repetition
        
        # set time designator
        time_designator = self.set_time_designator(self.time_btw_task_repetitions)
        repetition_pattern.Interval = f"P{time_designator}{self.time_btw_task_repetitions}"
        print(f'repetition_pattern.Interval:{repetition_pattern.Interval}')
        
        # Create action
        TASK_ACTION_EXEC = 0
        action = task_def.Actions.Create(TASK_ACTION_EXEC)
        action.ID = self.action_id
        action.Path = self.action_path
        action.WorkingDirectory = self.action_work_dir
        action.Arguments = self.action_args

        # Set parameters
        task_def.Principal.RunLevel = 1
        task_def.RegistrationInfo.Description = self.description
        task_def.Settings.Enabled = True
        task_def.Settings.StopIfGoingOnBatteries = False

        # Register task
        # If task already exists, it will be updated
        TASK_CREATE_OR_UPDATE = 6
        TASK_LOGON_NONE = 0
        try:
            self.root_folder.RegisterTaskDefinition(
                self.task_name,  # Task name
                task_def,
                TASK_CREATE_OR_UPDATE,
                '',  # No user
                '',  # No password
                TASK_LOGON_NONE)
        except pywintypes.com_error:
            return False
        return True
