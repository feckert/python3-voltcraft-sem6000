import threading

def DisconnectAfterTimeout(timeout):
    def Decorator(function):
        def decorated_function(*s, **d):
            def disconnect():
                disconnectable = s[0]
                disconnectable.disconnect()

            timer = threading.Timer(timeout, disconnect)
            timer.start()
   
            return_value = None 
            try:
                return_value = function(*s, **d)
            finally:
                timer.cancel()
    
            return return_value

        return decorated_function

    return Decorator

