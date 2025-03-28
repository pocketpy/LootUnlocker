import random
import hashlib
import uuid

class Version:
    def __init__(self, major: int, minor: int, patch: int):
        assert 0 <= major < 100
        assert 0 <= minor < 100
        assert 0 <= patch < 100
        self.major = major
        self.minor = minor
        self.patch = patch
        
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def __repr__(self):
        return f"Version({self.major}, {self.minor}, {self.patch})"
    
    def to_int32(self):
        return self.major * 10000 + self.minor * 100 + self.patch
    
    @staticmethod
    def from_int32(number: int):
        major, number = divmod(number, 10000)
        minor, patch = divmod(number, 100)
        return Version(major, minor, patch)
    

def random_number(length: int):
    return ''.join(random.choices('0123456789', k=length))

def random_passwd():
    prefix = random_number(16)
    return prefix + '-' + uuid.uuid4().hex

def hash_passwd(passwd: str):
    return hashlib.sha256((passwd + 'zhs6282').encode()).hexdigest()
