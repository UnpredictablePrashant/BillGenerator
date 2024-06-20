import csv
import random
from datetime import datetime, timedelta

def generate_dates(month, year, num_dates):
    """ Generate sorted dates and times within a given month and year """
    start_date = datetime(year, month, 1)
    end_date = start_date + timedelta(days=28)  
    dates = []
    for _ in range(num_dates):
        random_number_of_days = random.randrange(0, end_date.day - start_date.day)
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        new_date = start_date + timedelta(days=random_number_of_days)
        new_time = f"{random_hour:02}:{random_minute:02}"
        dates.append((new_date, new_time))
    dates.sort()  
    return [(date.strftime('%d/%m/%Y'), time) for date, time in dates]

def generate_csv(month, year, total_amount, rate, vehicle_number):
    """ Generate a CSV file with random data for a specific month and year based on a given rate and total amount """
    data = []
    min_amount = 500  
    max_amount = 5000 
    remaining_amount = total_amount

    estimated_entries = int(total_amount // ((min_amount + max_amount) / 2))
    num_entries = max(6, estimated_entries + 5)  

    receipt_numbers = sorted(random.randint(100000, 999999) for _ in range(num_entries))
    dates_and_times = generate_dates(month, year, num_entries) 

    index = 0
    while remaining_amount > max_amount:
        amount = random.randint(min_amount, max_amount)
        volume = round(amount / rate, 2)
        remaining_amount -= amount
        date, time = dates_and_times[index]
        data.append({
            "ReceiptNo": str(receipt_numbers[index]),
            "Rate": str(round(rate,2)),
            "Volume": str(volume),
            "Amount": str(amount),
            "Date": date,
            "Time": time,
            "VehicleNo": vehicle_number
        })
        index += 1

    if remaining_amount >= min_amount:
        volume = round(remaining_amount / rate, 2)
        date, time = dates_and_times[index]
        data.append({
            "ReceiptNo": str(receipt_numbers[index]),
            "Rate": str(round(rate,2)),
            "Volume": str(volume),
            "Amount": str(remaining_amount),
            "Date": date,
            "Time": time,
            "VehicleNo": vehicle_number
        })

    with open('petroldetails.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

month = int(input("Enter the month (1-12): "))
year = int(input("Enter the year (e.g., 2024): "))
rate = float(input("Enter the rate for the month: "))
total_amount = float(input("Enter the total amount for which to generate the bills: "))
vehicle_number = input("Enter your vehicle no.: ")

generate_csv(month, year, total_amount, rate, vehicle_number)
