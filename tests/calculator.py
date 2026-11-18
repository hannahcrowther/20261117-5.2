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

if __name__ == "__main__":
    myCalc = Calculator(a=5, b=6)
    print(myCalc.get_sum())

