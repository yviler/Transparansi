from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def getPasswordHash(password):
    return password_hash.hash(password)

def verifyPasswordWithHash(password, hashed):
    return password_hash.verify(password, hashed)