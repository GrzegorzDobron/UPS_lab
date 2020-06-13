class CircularBuffer(object):
    buffer = []
    write = 0
    read = 0
    N = 0

    def __init__(self, N):
        for i in range(N):
            self.buffer.append([0,0])
        self.N = N
    
    def putElements(self, elements):
        num = len(elements)
        if (((self.N-1) - self.length()) < num):
            return 1
        for i in range(num):
            self.put(elements[i])
        return 0
    
    def put(self, element):
        if(self.write == (self.read-1) & (self.N-1)):
            return 1
        self.buffer[self.write] = element
        self.write = (self.write + 1) & (self.N-1)
        return 0
        
    def getElements(self, N):
        elements = []
        if (self.length() < N):
            return [1]
        for i in range(N):
            element = self.get()
            elements.append([element[1][0], element[1][1]])
        return elements
        
    def get(self):
        if(self.write == self.read):
            return [1]
        data = self.buffer[self.read]
        self.read= (self.read + 1) & (self.N - 1)
        return [0,data]

    def length(self):
        return (self.write - self.read) & (self.N-1);