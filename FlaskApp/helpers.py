import base64

def add_underscore(s):
    return '_'.join(s.split(' '))

def remove_underscore(s):
    return ' '.join(s.split('_'))

def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))
