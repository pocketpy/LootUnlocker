
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
    
    def to_number(self):
        return self.major * 10000 + self.minor * 100 + self.patch
    
    @staticmethod
    def from_number(number: int):
        major, number = divmod(number, 10000)
        minor, patch = divmod(number, 100)
        return Version(major, minor, patch)