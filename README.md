# Vehicle Rental System
Welcome to the Vehicle Rental System! This platform allows users to browse, book, and manage car and bike rentals conveniently. The system is built using Django and PostgreSQL and is deployed on Render.

# Deployed Project
The project is currently deployed and accessible at:   <a href="https://vehiclerentalsystem-fh4d.onrender.com/" target="_blank">VehicleRentalSystem</a>

## Features
* Browse available cars and bikes for rent
* Check vehicle availability in real time
* Book vehicles online
* Manage bookings easily through a user-friendly interface
* Dealer management of vehicle listings

## Getting Started Locally
To run the project on your local machine, follow these steps:

# Prerequisites
Ensure you have the following installed:

* Python 3.12
* Django
* PostgreSQL
* Git
* Virtualenv

# Installation

* Clone the repository
git clone https://github.com/gabrielouma/VehicleRentalSystem.git

cd vehicle-rental-system

* Create a virtual environment
virtualenv venv
source venv/bin/activate  # For Linux/macOS
# OR
venv\Scripts\activate  # For Windows

* Install the dependencies
pip install -r requirements.txt

* Configure the database

- Create a new PostgreSQL database:
createdb vehiclerentalsystem

- Update the DATABASES settings in settings.py with your local database credentials:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vehiclerentalsystem',
        'USER': 'your_postgres_user',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

* Run migrations

python manage.py makemigrations

* Migrate the database

python manage.py migrate

* Create superuser
To access the Django admin panel and manage the system, create a superuser account:

python manage.py createsuperuser

* Run the server

python manage.py runserver

* Access the site
pen your web browser and go to http://127.0.0.1:8000/ to access the application locally.

# Deployment
To deploy this project to production, you can use platforms like Render or Heroku. Below are the deployment steps for Render:

- Create an account and log in to Render.
- Create a new Web Service and link it to your GitHub repository.
- Set up environment variables, including:
DATABASE_URL for the PostgreSQL connection string.
- Set DEBUG=False for production environments.
- Push your repository and let Render handle the deployment.

# Support
If you have any questions or need help, please contact us at [oumagaby01@gmail.com](mailto:oumagaby01@gmail.com).

# License
This project is licensed under the MIT License.







<!-- # Vehicle Rental System (Django)
This is a Django-based vehicle rental platform for cars and bikes, allowing users to browse, book, and pay for rentals online. The platform provides a seamless experience for managing vehicle rentals, ensuring convenience for both users and service providers.

# Features
Vehicle Listings: Browse a variety of cars and bikes with detailed descriptions, pricing, and photos.
Availability Check: Real-time availability of vehicles to avoid double bookings.
Booking Management: Users can book vehicles, view their booking history, and manage existing bookings.
Secure Payments: Integrated payment gateways for safe and reliable online payments.
Admin Panel: Comprehensive admin dashboard to manage vehicles, bookings, and users.
User Authentication: Secure registration, login, and password management.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/vehicle-rental-system.git
cd vehicle-rental-system
Set up a virtual environment:

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

bash
Copy code
python manage.py migrate
Run the server:

bash
Copy code
python manage.py runserver
Access the application: Open your browser and go to http://127.0.0.1:8000/.

Configuration
Database: The project uses a default SQLite database. To switch to PostgreSQL or any other database, update the DATABASES setting in settings.py.
Payment Integration: Payment integration (e.g., PayPal, Stripe) can be configured in the payments module. Ensure to add your API keys in the environment variables or settings.
Contributing
Feel free to contribute to this project by creating a pull request or opening an issue.

License
This project is licensed under the MIT License - see the LICENSE file for details. -->