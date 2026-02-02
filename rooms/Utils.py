import random
import string

def generate_unique_room_number(model_instance):    
    length = 6
    characters = string.ascii_uppercase + string.digits
    
    while True:
        random_code = ''.join(random.choice(characters) for _ in range(length))
        
        if not model_instance.__class__.objects.filter(room_number=random_code).exists():
            return random_code