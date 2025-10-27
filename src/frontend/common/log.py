import streamlit as st

class LogLevels:
    INFO='info'
    WARNING='warning'
    ERROR='error'
    SUCCESS='success'


class Log():
    def __init__(self):
        self.level = LogLevels()
        self.__messages = []

    @property
    def has_logs(self):
        return self.__messages

    def append(self, msg: str, level: LogLevels, icon=None):
        self.__messages.append({'msg': msg, 'level': level, 'icon': icon})

    def render(self):
        if self.__messages:
            msg = self.__messages[0]
            self.__messages.pop(0)
            if msg['level'] == self.level.INFO:
                st.info(msg['msg'], icon=msg['icon'])

            elif msg['level'] == self.level.WARNING:
                st.warning(msg['msg'], icon=msg['icon'])

            elif msg['level'] == self.level.ERROR:
                st.error(msg['msg'], icon=msg['icon'])
                
            elif msg['level'] == self.level.SUCCESS:
                st.success(msg['msg'], icon=msg['icon'])

            else:
                st.error(f'Unsuported Log-level: {msg["level"]}')

    