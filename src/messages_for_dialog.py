messages = {'delete_task_success': {'title': "The task was deleted", 'message': "The task was deleted because the folder of images that was specified during the creation of the task was deleted or moved."},
            'delete_task_failed': {'title': "The task has not been deleted", 'message': "The task has not been deleted. Please try again while running the program as administrator."},
            'change_wall_success': {'title': "The wallpaper has been changed", 'message': "The wallpaper on the desktop has been changed successfully"},
            'change_wall_failed': {'title': "The wallpaper hasn't been changed", 'message': "The wallpaper on the desktop hasn't been changed successfully."},
            'download_wall_success': {'title': "The wallpaper was successfully downloaded", 'message': "The wallpaper was successfully downloaded from Unsplash."},
            'download_wall_failed': {'title': "The wallpaper wasn't successfully downloaded", 'message': "The wallpaper wasn't successfully downloaded from Unsplash."},
            'create_task_success': {'title': "Task created successfully", 'message': "The task will be called after the time that you set."},
            'create_task_failed': {'title': "Task not created", 'message': "To successfully create a task, this program must be run as administrator. Please restart the program with administrator privileges and try again."}
            }

def get_title_and_message(event):
    return messages[event]