import pdfkit
import random
from jinja2 import Template

# HTML Template with Jinja2 placeholders
html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 600px;
            margin: auto;
            border: 1px solid #ccc;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: bold;
        }

        .sub-header {
            text-align: center;
            margin-bottom: 20px;
        }

        .sub-header p {
            margin: 5px 0;
            font-size: 14px;
        }

        .section {
            margin-bottom: 20px;
        }

        .section-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .details {
            line-height: 1.6;
        }

        .details p {
            margin: 0;
        }

        .terms {
            font-size: 12px;
            color: #555;
            margin-top: 20px;
        }

        .terms p {
            margin: 0;
            margin-bottom: 10px;
        }

        .fare-details {
            font-size: 16px;
            font-weight: bold;
        }

        .fare-details p {
            margin: 5px 0;
        }

        .note {
            font-size: 12px;
            color: red;
            margin-top: 20px;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <h1>eTICKET</h1>
            <p>Congratulations! You have booked a reschedulable ticket. You can advance or postpone this journey till {{ post_date }}.</p>
        </div>

        <div class="sub-header">
            <h2>Shivam Travels</h2>
            <p>No G 1/5, H, New Palam Vihar Phase 1, Gurugram, Haryana 122017</p>
        </div>

        <div class="section">
            <div class="section-title">Journey Details</div>
            <div class="details">
                <p><strong>From:</strong> Delhi</p>
                <p><strong>To:</strong> {{ dropping_point }}</p>
                <p><strong>Date:</strong> {{ date }}</p>
                <p><strong>Ticket no:</strong> {{ ticket_no }}</p>
                <p><strong>PNR no:</strong> {{ pnr_no }}</p>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Passenger Details</div>
            <div class="details">
                <p><strong>Name:</strong> {{ name }}</p>
                <p><strong>Age:</strong> {{ age }}</p>
                <p><strong>Gender:</strong> {{ gender }}</p>
                <p><strong>Seat Number:</strong> {{ seat_number }}</p>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Boarding & Dropping Point</div>
            <div class="details">
                <p><strong>Boarding Point:</strong> Delhi, Kashmiri Gate</p>
                <p><strong>Departure Time:</strong> 12:00</p>
                <p><strong>Dropping Point:</strong> {{ dropping_point }}</p>
                <p><strong>Dropping Point Time:</strong> 15:15 on {{ drop_date }}</p>
            </div>
        </div>

        <div class="section fare-details">
            <div class="section-title">Fare Details</div>
            <p><strong>Total Fare:</strong> ₹{{ total_fare }}</p>
            <p><strong>Net amount:</strong> ₹{{ net_amount }}</p>
            <p><strong>Taxable amount:</strong> ₹{{ taxable_amount }}</p>
        </div>

        <div class="terms">
            <p><strong>Terms & Conditions:</strong></p>
            <p>Each passenger is allowed to carry one bag of up to 10 kgs and one personal item such as a laptop bag, handbag, or briefcase of up to 5 kgs.</p>
            <p>Passengers should not carry any goods like weapons, inflammable, firearms, ammunition, drugs, liquor, smuggled goods, etc., and any other articles that are prohibited under law.</p>
            <p>The travel operator reserves the right to deny boarding or charge an additional amount in case a passenger is traveling with extra luggage than what is mentioned above.</p>
            <p>Partial Cancellation is NOT allowed for this ticket. Charges for complete ticket cancellation are as mentioned:</p>
            <ul>
                <li><strong>After 12:00 on {{ cancellation_date }}:</strong> ₹{{ total_fare }}</li>
                <li><strong>Before 12:00 on {{ cancellation_date }}:</strong> ₹{{ cancellation_fee }} will be cut as cancellation charges</li>
            </ul>
        </div>

        <div class="note">
            <p>NOTE: This operator accepts mTicket, you need not carry a printout.</p>
        </div>
    </div>
</body>

</html>
"""

def generate_ticket_data():
    ticket_no = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
    pnr_no = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))
    seat_number = random.randint(1, 40)
    total_fare = random.randint(3000, 5000)
    net_amount = round(total_fare * 0.8474, 2)  # Assuming 18% GST
    taxable_amount = round(total_fare * 0.1526, 2)
    cancellation_fee = round(total_fare * 0.0909, 2)
    return ticket_no, pnr_no, seat_number, total_fare, net_amount, taxable_amount, cancellation_fee

def create_pdf(to, date, name, age, gender, dropping_point):
    ticket_no, pnr_no, seat_number, total_fare, net_amount, taxable_amount, cancellation_fee = generate_ticket_data()
    
    # Post date can be advanced or postponed by 30 days from the given date
    post_date = (date.split()[0] + " Jul 2024")
    
    # Filling the template
    template = Template(html_template)
    rendered_html = template.render(
        date=date,
        post_date=post_date,
        name=name,
        age=age,
        gender=gender,
        dropping_point=dropping_point,
        ticket_no=ticket_no,
        pnr_no=pnr_no,
        seat_number=seat_number,
        total_fare=total_fare,
        net_amount=net_amount,
        taxable_amount=taxable_amount,
        cancellation_fee=cancellation_fee,
        drop_date=str(int(date.split()[0])+1) + " Jul 2024",
        cancellation_date = date.split()[0] + " Jul 2024"
    )
    
    # Generate PDF
    pdfkit.from_string(rendered_html, 'ticket_invoice.pdf')

# Example usage
create_pdf(to="Gwalior Bus stand", date="14 Jul 2024", name="Shubham", age=28, gender="Male", dropping_point="Gwalior Bus stand")
