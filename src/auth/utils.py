import bcrypt
import base64

def hashpw(password: str)->str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return base64.b64encode(hashed).decode('utf-8')

def checkpw(password: str, target: str)->bool:
    hashed_bytes = base64.b64decode(target.encode('utf-8'))
    return bcrypt.checkpw(password.encode('utf-8'), hashed_bytes)
