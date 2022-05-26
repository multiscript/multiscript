

class PlanMonitor:
    '''This class observes an instance of the PlanRunner class.
    '''    
    def allow_cancel(self):
        pass

    def set_progress_percent(self, progress):
        '''Set the progress percent as an integer between 0 and 100
        '''
        pass

    def set_status_text(self, text):
        pass

    def set_substatus_text(self, text):
        pass

    def request_confirmation(self, message=None, path=None):
        pass


class PlanMonitorCollection(PlanMonitor):
    '''Maintains a collection of PlanMonitors, and makes it easy to call them.
    '''
    def __init__(self, runner, monitor=None):
        self.runner = runner
        self._monitors = set()
        if monitor is not None:
            self.add_monitor(monitor)

    def add_monitor(self, plan_monitor):
        self._monitors.add(plan_monitor)
    
    def remove_monitor(self, plan_monitor):
        self._monitors.remove(plan_monitor)

    #
    # PlanMonitor methods
    #

    def allow_cancel(self):
        for monitor in self._monitors:
            monitor.allow_cancel()

    def set_progress_percent(self, progress):
        for monitor in self._monitors:
            monitor.set_progress_percent(progress)

    def set_status_text(self, text):
        for monitor in self._monitors:
            monitor.set_status_text(text)
        
    def set_substatus_text(self, text):
        for monitor in self._monitors:
            monitor.set_substatus_text(text)

    def request_confirmation(self, message=None, path=None):
        if not self.runner.plan.config.general.allow_confirmations:
            return

        for monitor in self._monitors:
            monitor.request_confirmation(message, path)
