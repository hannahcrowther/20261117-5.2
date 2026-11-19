class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.hannah = 2.45

    def get_sum(self):
        return self.a + self.b
    
    def hannah_index(self):
        ans = (self.a + self.b)*self.hannah
        return ans
    
    def get_minus(self):
        return self.a - self.b
    
    def get_division(self):
        return self.a/self.b
    
    def get_product(self):
        return self.a * self.b


myCalc = Calculator(a=247, b=12)
myans = myCalc.get_division()

    # WRITE myans to a text file inside /data

with open("/data/demofile.txt", "a") as f:
  f.write(myans)