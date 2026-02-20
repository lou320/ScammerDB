# ScammerDB 🛡️

A web-based database application designed to store, search, and track information about scammers, with a primary focus on protecting the Myanmar community. 

This platform allows users to safely log and verify reports, helping to prevent fraud and raise awareness within the community.

## 🚀 Features
* **Searchable Database:** Quickly search for known scammer profiles, aliases, or contact information.
* **Reporting System:** Securely log new scammer information into the database.
* **Community Protection:** Specifically tailored to address and track localized scams affecting the Myanmar community.
* **Admin Dashboard:** Secure backend for managing database entries and verifying user-submitted reports.

## 🛠️ Tech Stack
* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript (Template rendering)
* **Database:** SQLite / PostgreSQL (Configure in `settings.py`)

## ⚙️ Local Installation & Setup

If you want to run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/lou320/ScammerDB.git](https://github.com/lou320/ScammerDB.git)
   cd ScammerDB
Create a virtual environment (Recommended):

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Apply database migrations:

Bash
python manage.py migrate
Run the development server:

Bash
python manage.py runserver
The application will be available at http://127.0.0.1:8000/

📈 Future Roadmap
Implement user authentication for verified reporting.

Add an API endpoint for third-party integrations.

Integrate automated OSINT tools to verify scammer details.
