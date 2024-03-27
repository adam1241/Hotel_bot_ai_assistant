import csv
def read_csv_file( name, email) :
    filename = "Clients.csv"
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if  name.lower() in row["name"].lower() and row["email"] == email:
                data.append({
                    "name": row["name"],
                    "email": row["email"],
                    "spa": row["spa"] == "True",
                    "luggage": row["luggage"] == "True",
                    "cib": row["cib"] == "True",
                    "bill": float(row["bill"]),
                    "loyalty": row["loyalty"] == "True",
                    "payment": row["payment"] == "True",
                    "payment_method": row["payment_method"],
                    "room_booked": row["room_booked"],
                    "time_room": row["time_room"],
                    "extra_bed": row["extra_bed"] == "True"
                })
                return data
    return None
def addClient( name,email,  time_room,) :
    # Append the new booking to the Clients.csv file
    with open("Clients.csv", "a", newline="") as file:
        writer = csv.writer(file)
        print("i am adding a row")
        writer.writerow([name, email, "False", "False", "False", "11111", "False", "True", "credit card", "false", time_room, "false"])

def run() :
    name = "Yannisou"
    email = "yannis.haralambous@imt-atlantique.fr"
    data = read_csv_file(name, email)
    time_room=""
    if data==None:
        addClient(name,email, time_room) 
        print("You are a new client, welcome to our hotel! If you are already a client, please ask me to repeat collecting your info.")
    else:
        print("Welcome back sir, how can I help you?")
    return []

import random
import string

def generate_random_email():
    # Generate a random username
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Generate a random domain name
    domain = ''.join(random.choices(string.ascii_lowercase, k=5))

    # Generate a random top-level domain (TLD)
    tld = random.choice(['com', 'org', 'net', 'edu', 'gov'])

    # Combine the components to form the email address
    email = f"- [{username}@{domain}.{tld}](email)"

    return email

def generate_random_name():
    name_length = random.randint(3, 20)
    name = ''.join(random.choices(string.ascii_letters, k=name_length))
    return name

def generate_random_names(num_names=100):
    names = [generate_random_name() for _ in range(num_names)]
    return names

# Generate 100 random names
random_names = generate_random_names()
for i in random_names:
    print(f'- [{i}](name)')