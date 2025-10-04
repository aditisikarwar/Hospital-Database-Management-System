
# 🏥 Hospital Management System (DBMS Project)  
### *Designed & Developed by Aditi Sikarwar*  
**Final Year B.Tech Biotechnology | NIT Durgapur | May 2024**

---

![Project Banner](https://tse3.mm.bing.net/th/id/OIP.fFjPQml38ISpOLYiOStBTgHaFj?cb=12&pid=Api)

---

## 📘 Project Overview

The **Hospital Management System (HMS)** is a database-driven web application built to **digitize and streamline hospital operations** — including **patient management**, **doctor scheduling**, **appointments**, **admissions**, and **billing**.  

This project was created as part of **Database Management Systems coursework (May 2024)**.  
It demonstrates the use of **MySQL**, **Flask (Python)**, and **HTML/CSS/JavaScript** for building a scalable and interactive database-backed system.

---

## 🎯 Objectives

- Design a **normalized MySQL database** for hospital data.  
- Implement **entity relationships** among core components (patients, doctors, rooms, bills).  
- Provide **CRUD functionality** for hospital operations.  
- Develop a **simple web interface** for data entry and retrieval.  
- Optimize database efficiency through indexing and entity relationships.

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask Framework) |
| Database | MySQL |
| ORM | SQLAlchemy |
| Tools | VS Code, XAMPP / MySQL Workbench, Postman |
| Version Control | Git & GitHub |

---

## 🧩 Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    PATIENT {
        INT id PK
        VARCHAR name
        DATE dob
        VARCHAR gender
        VARCHAR phone
        VARCHAR email
        VARCHAR address
    }
    DOCTOR {
        INT id PK
        VARCHAR name
        INT department_id FK
        VARCHAR qualification
        VARCHAR phone
        VARCHAR email
    }
    DEPARTMENT {
        INT id PK
        VARCHAR name
        VARCHAR location
    }
    APPOINTMENT {
        INT id PK
        INT patient_id FK
        INT doctor_id FK
        DATETIME appt_datetime
        VARCHAR reason
        VARCHAR status
    }
    ROOM {
        INT id PK
        VARCHAR room_number
        VARCHAR type
        BOOLEAN is_available
    }
    ADMISSION {
        INT id PK
        INT patient_id FK
        INT room_id FK
        DATETIME admit_date
        DATETIME discharge_date
        VARCHAR reason
    }
    BILL {
        INT id PK
        INT admission_id FK
        DECIMAL amount
        DATE bill_date
        VARCHAR status
    }

    PATIENT ||--o{ APPOINTMENT : "books"
    DOCTOR ||--o{ APPOINTMENT : "has"
    DOCTOR }o--|| DEPARTMENT : "belongs_to"
    DEPARTMENT ||--o{ DOCTOR : "has"
    ROOM ||--o{ ADMISSION : "used_in"
    PATIENT ||--o{ ADMISSION : "admitted_to"
    ADMISSION ||--o{ BILL : "generates"
````

---

## 🗄️ Database Features

* **Relational schema design** (3NF normalized)
* **Primary & Foreign key constraints** for referential integrity
* **ENUM & CHECK constraints** for controlled values
* **Cascading relationships** (e.g., patient deletion removes appointments)
* **Indexing** for faster search on patient name & appointment date
* **Sample data** provided via `sample_data.sql`

---

## ⚙️ Installation & Setup

### Prerequisites

* Python ≥ 3.8
* MySQL ≥ 8.0
* `pip` and virtual environment tools

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/aditi-sikarwar/Hospital-Management-System.git
cd Hospital-Management-System
```

### 2️⃣ Configure Database

Create a MySQL database and user:

```sql
CREATE DATABASE hospital_db;
CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'hms_pass';
GRANT ALL PRIVILEGES ON hospital_db.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;
```

Import schema and sample data:

```bash
mysql -u root -p hospital_db < schema.sql
mysql -u root -p hospital_db < sample_data.sql
```

### 3️⃣ Install Dependencies

```bash
python -m venv venv
source venv/bin/activate    # (Linux/Mac)
venv\Scripts\activate       # (Windows)
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python app.py
```

Now open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 🧠 Key Functionalities

* 👩‍⚕️ **Patient Management** – Add, view, and search patient records.
* 🩺 **Doctor & Department Management** – Manage doctor details and assign them to departments.
* 📅 **Appointments** – Book, view, or cancel patient appointments.
* 🛏️ **Admissions & Rooms** – Manage patient admissions, discharges, and room availability.
* 💳 **Billing System** – Generate bills linked to admissions.
* 📊 **Logs & Audits** – Track actions in the activity log table.

---

## 💻 Project Demonstration

### ▶️ Working Snapshots

> Replace these placeholders with actual screenshots once your project is running locally.

| Feature                     | Screenshot                        |
| --------------------------- | --------------------------------- |
| Home Page                   | ![](screenshots/home.png)         |
| Patients Management         | ![](screenshots/patients.png)     |
| Appointments Page           | ![](screenshots/appointments.png) |
| Database in MySQL Workbench | ![](screenshots/database.png)     |
| ER Diagram                  | ![](screenshots/er-diagram.png)   |

> 📸 To capture screenshots:
> Run the project → open in browser → take screenshots using Snipping Tool or Print Screen → save in `/screenshots/` folder.

---

## 🧾 Sample API Endpoints

| Method | Endpoint                         | Description           |
| ------ | -------------------------------- | --------------------- |
| GET    | `/api/patients`                  | Fetch all patients    |
| POST   | `/api/patients`                  | Add a new patient     |
| GET    | `/api/appointments`              | View all appointments |
| POST   | `/api/appointments`              | Create appointment    |
| POST   | `/api/admissions`                | Admit a patient       |
| POST   | `/api/admissions/{id}/discharge` | Discharge patient     |
| POST   | `/api/bills`                     | Generate bill         |

---

## 🚀 Future Enhancements

* Authentication (Admin / Doctor / Receptionist)
* Dashboard with charts and analytics
* Email or SMS appointment reminders
* Export reports (PDF/CSV)
* Cloud deployment (AWS / Render / Railway)
* Enhanced UI using React or Bootstrap

---

## 👩‍🎓 Author

**👩‍💻 Aditi Sikarwar**
Final Year B.Tech (Biotechnology)
National Institute of Technology, Durgapur
📅 Internship Project — May 2024
📧 *[aditisikarwar777@gmail.com](mailto:aditi.sikarwar@example.com)*
🔗 [LinkedIn](https://www.linkedin.com/in/aditi-sikarwar) | [GitHub](https://github.com/aditi-sikarwar)

---

## 📜 License

This project is licensed under the **MIT License** – you are free to use and modify it for educational purposes.

```
MIT License  
Copyright (c) 2024 
Permission is hereby granted, free of charge, to any person obtaining a copy...
```

---

### 🌟 If you like this project, don’t forget to ⭐ star the repository on GitHub!


