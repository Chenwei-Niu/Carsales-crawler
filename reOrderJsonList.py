import json
import random
class Shuffler:
    def __init__(self):
        self.original_file = open("D:\\carsalesData\\car_data.json",'r',encoding='utf-8')
        self.shuffled_file = open("D:\\carsalesData\\shuffled_car_data.json",'w',encoding='utf-8')
    
    def reOrder(self):
        lst = []
        lst = json.load(self.original_file)
        random.shuffle(lst)
        return json.dumps(lst)

if __name__ == "__main__":
    shuffler = Shuffler() # instantiate
    lst = shuffler.reOrder()
    

    shuffler.shuffled_file.write(str(lst).replace("'",""))

    shuffler.shuffled_file.close
    shuffler.original_file.close