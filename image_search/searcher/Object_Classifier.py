from ultralytics import YOLO
def Decoder(classid):
    class_map = {
        '0': "Person",
        '1': "Bicycle",
        '2': "Car",
        '3': "Motorcycle",
        '4': "Airplane",
        '5': "Bus",
        '6': "Train",
        '7': "Truck",
        '8': "Boat",
        '9': "Traffic Light",
        '10': "Fire Hydrant",
        '11': "Stop Sign",
        '12': "Parking Meter",
        '13': "Bench",
        '14': "Bird",
        '15': "Cat",
        '16': "Dog",
        '17': "Horse",
        '18': "Sheep",
        '19': "Cow",
        '20': "Elephant",
        '21': "Bear",
        '22': "Zebra",
        '23': "Giraffe",
        '24': "Backpack",
        '25': "Umbrella",
        '26': "Handbag",
        '27': "Tie",
        '28': "Suitcase",
        '29': "Frisbee",
        '30': "Skis",
        '31': "Snowboard",
        '32': "Sports Ball",
        '33': "Kite",
        '34': "Baseball Bat",
        '35': "Baseball Glove",
        '36': "Skateboard",
        '37': "Surfboard",
        '38': "Tennis Racket",
        '39': "Bottle",
        '40': "Wine Glass",
        '41': "Cup",
        '42': "Fork",
        '43': "Knife",
        '44': "Spoon",
        '45': "Bowl",
        '46': "Banana",
        '47': "Apple",
        '48': "Sandwich",
        '49': "Orange",
        '50': "Broccoli",
        '51': "Carrot",
        '52': "Hot Dog",
        '53': "Pizza",
        '54': "Donut",
        '55': "Cake",
        '56': "Chair",
        '57': "Couch",
        '58': "Potted Plant",
        '59': "Bed",
        '60': "Dining Table",
        '61': "Toilet",
        '62': "TV",
        '63': "Laptop",
        '64': "Mouse",
        '65': "Remote",
        '66': "Keyboard",
        '67': "Cell Phone",
        '68': "Microwave",
        '69': "Oven",
        '70': "Toaster",
        '71': "Sink",
        '72': "Refrigerator",
        '73': "Book",
        '74': "Clock",
        '75': "Vase",
        '76': "Scissors",
        '77': "Teddy Bear",
        '78': "Hair Dryer",
        '79': "Toothbrush"
    }
    
    return class_map.get(str(classid), "Unknown")
def classify():
    model = YOLO("yolov8l.pt")
    results = model.predict("temp/stored_picture.png", save_txt=True)
    file_path="runs/detect/predict/labels/stored_picture.txt"
    try:
     with open(file_path, 'r') as file:
         first_number = None
         first_number = file.read(1)  # Attempt to convert line to integer  # Exit loop as soon as the first integer is found
    except FileNotFoundError:
        return None
    first_number = first_number.replace(" ", "")
    text = Decoder(first_number)
    return text
    


