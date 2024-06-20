import csv
import os
from PIL import Image, ImageDraw, ImageFont

def fill_bill(image_path, values, output_folder):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("times.ttf", 13.2)
    except IOError:
        font = ImageFont.load_default()

    positions = {
        "VehicleNo": (121,525),
        "ReceiptNo": (151, 323),
        "Rate": (151, 450),
        "Volume": (151, 469),
        "Amount": (151, 490),
        "Date": (75, 580),
        "Time": (207, 580)
    }

    blue_color = (16, 30, 136)
    for key, position in positions.items():
        draw.text(position, values[key], blue_color, font=font)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    new_image_path = os.path.join(output_folder, f'filled_bill_{values["ReceiptNo"]}.png')
    image.save(new_image_path)
    return new_image_path

def generate_bills_from_csv(csv_path, image_path, output_folder):
    image_paths = []
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            new_image_path = fill_bill(image_path, row, output_folder)
            image_paths.append(new_image_path)
            print(f"Bill has been filled and saved to {new_image_path}")
    return image_paths

def create_combined_pdf(image_paths, output_folder):
    images = [Image.open(x).convert('RGB') for x in image_paths]
    pdf_path = os.path.join(output_folder, "combined_bills.pdf")
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"Combined PDF created at {pdf_path}")

csv_path = 'petroldetails.csv'  
image_path = './emptybill.png'  
output_folder = './bills_output'

image_paths = generate_bills_from_csv(csv_path, image_path, output_folder)

create_combined_pdf(image_paths, output_folder)
