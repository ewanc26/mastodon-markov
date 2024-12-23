import warnings

def ignore_future_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)