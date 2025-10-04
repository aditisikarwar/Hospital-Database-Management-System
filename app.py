# app.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime
import decimal

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)

# ---------- Models ----------
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    qualification = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    department = db.relationship('Department', backref='doctors')

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum('Male','Female','Other'), default='Male')
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(30), unique=True, nullable=False)
    type = db.Column(db.Enum('General','Semi-Private','Private','ICU','OT'), default='General')
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appt_datetime = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255))
    status = db.Column(db.Enum('Scheduled','Completed','Cancelled','No-Show'), default='Scheduled')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

class Admission(db.Model):
    __tablename__ = 'admission'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    admit_date = db.Column(db.DateTime, nullable=False)
    discharge_date = db.Column(db.DateTime, nullable=True)
    reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    patient = db.relationship('Patient', backref='admissions')
    room = db.relationship('Room', backref='admissions')

class Bill(db.Model):
    __tablename__ = 'bill'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False)
    amount = db.Column(db.Numeric(12,2), default=0.00)
    bill_date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    status = db.Column(db.Enum('Unpaid','Paid','Pending'), default='Unpaid')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    admission = db.relationship('Admission', backref='bills')

class ActivityLog(db.Model):
    __tablename__ = 'activity_log'
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    action = db.Column(db.String(50))
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# ---------- Helpers ----------
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def patients_page():
    return render_template('patients.html')

@app.route('/appointments')
def appointments_page():
    return render_template('appointments.html')

# Dev-only endpoint to initialize DB from models (destructive)
@app.route('/init-db', methods=['POST'])
def init_db():
    db.drop_all()
    db.create_all()
    return jsonify({"message": "Database schema created (dev only)."}), 201

# Departments
@app.route('/api/departments', methods=['GET'])
def get_departments():
    deps = Department.query.all()
    return jsonify([{"id":d.id,"name":d.name,"location":d.location} for d in deps])

@app.route('/api/departments', methods=['POST'])
def create_department():
    data = request.json or {}
    name = data.get('name')
    if not name:
        return jsonify({"error":"name required"}), 400
    d = Department(name=name, location=data.get('location'))
    db.session.add(d)
    db.session.commit()
    return jsonify({"id": d.id, "name": d.name}), 201

# Patients
@app.route('/api/patients', methods=['GET'])
def list_patients():
    q = Patient.query
    name = request.args.get('name')
    if name:
        q = q.filter(Patient.name.ilike(f"%{name}%"))
    patients = q.all()
    out = []
    for p in patients:
        out.append({
            "id": p.id,
            "name": p.name,
            "dob": p.dob.isoformat() if p.dob else None,
            "gender": p.gender,
            "phone": p.phone,
            "email": p.email,
            "address": p.address
        })
    return jsonify(out)

@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json or {}
    if not data.get('name'):
        return jsonify({"error":"name is required"}), 400
    dob = None
    if data.get('dob'):
        try:
            dob = datetime.fromisoformat(data['dob']).date()
        except Exception:
            return jsonify({"error":"dob must be ISO date YYYY-MM-DD"}), 400
    p = Patient(
        name=data['name'],
        dob=dob,
        gender=data.get('gender','Male'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id, "name": p.name}), 201

@app.route('/api/patients/<int:pid>', methods=['GET'])
def get_patient(pid):
    p = Patient.query.get_or_404(pid)
    return jsonify({
        "id": p.id,
        "name": p.name,
        "dob": p.dob.isoformat() if p.dob else None,
        "gender": p.gender,
        "phone": p.phone,
        "email": p.email,
        "address": p.address
    })

# Appointments
@app.route('/api/appointments', methods=['GET'])
def list_appointments():
    appts = Appointment.query.order_by(Appointment.appt_datetime.desc()).all()
    out = []
    for a in appts:
        out.append({
            "id": a.id,
            "patient": {"id": a.patient.id, "name": a.patient.name},
            "doctor": {"id": a.doctor.id, "name": a.doctor.name},
            "appt_datetime": a.appt_datetime.isoformat(),
            "reason": a.reason,
            "status": a.status
        })
    return jsonify(out)

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json or {}
    try:
        dt = datetime.fromisoformat(data['appt_datetime'])
    except Exception:
        return jsonify({"error":"appt_datetime required as ISO datetime"}), 400
    # Basic existence checks
    if not data.get('patient_id') or not data.get('doctor_id'):
        return jsonify({"error":"patient_id and doctor_id required"}), 400
    # ensure patient/doctor exist
    if not Patient.query.get(data['patient_id']):
        return jsonify({"error":"patient not found"}), 404
    if not Doctor.query.get(data['doctor_id']):
        return jsonify({"error":"doctor not found"}), 404
    a = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        appt_datetime=dt,
        reason=data.get('reason'),
        status=data.get('status','Scheduled')
    )
    db.session.add(a)
    db.session.commit()
    return jsonify({"id": a.id}), 201

@app.route('/api/appointments/<int:aid>', methods=['PATCH'])
def update_appointment(aid):
    a = Appointment.query.get_or_404(aid)
    data = request.json or {}
    if 'status' in data:
        a.status = data['status']
    if 'appt_datetime' in data:
        try:
            a.appt_datetime = datetime.fromisoformat(data['appt_datetime'])
        except Exception:
            return jsonify({"error":"appt_datetime must be ISO datetime"}), 400
    db.session.commit()
    return jsonify({"id": a.id, "status": a.status})

# Rooms
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{"id":r.id,"room_number":r.room_number,"type":r.type,"is_available":r.is_available} for r in rooms])

# Admissions
@app.route('/api/admissions', methods=['POST'])
def create_admission():
    data = request.json or {}
    try:
        admit_date = datetime.fromisoformat(data['admit_date'])
    except Exception:
        return jsonify({"error":"admit_date required as ISO datetime"}), 400
    patient_id = data.get('patient_id')
    room_id = data.get('room_id')
    if not patient_id or not room_id:
        return jsonify({"error":"patient_id and room_id required"}), 400
    if not Patient.query.get(patient_id):
        return jsonify({"error":"patient not found"}), 404
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error":"room not found"}), 404
    if not room.is_available:
        return jsonify({"error":"room not available"}), 400
    admission = Admission(patient_id=patient_id, room_id=room_id, admit_date=admit_date, reason=data.get('reason'))
    room.is_available = False
    db.session.add(admission)
    db.session.commit()
    return jsonify({"id": admission.id}), 201

@app.route('/api/admissions/<int:aid>/discharge', methods=['POST'])
def discharge(aid):
    adm = Admission.query.get_or_404(aid)
    if adm.discharge_date:
        return jsonify({"error":"already discharged"}), 400
    adm.discharge_date = datetime.now()
    adm.room.is_available = True
    db.session.commit()
    return jsonify({"id": adm.id, "discharge_date": adm.discharge_date.isoformat()})

# Bills
@app.route('/api/bills', methods=['POST'])
def create_bill():
    data = request.json or {}
    admission_id = data.get('admission_id')
    amount = data.get('amount', 0.0)
    if not admission_id:
        return jsonify({"error":"admission_id required"}), 400
    if not Admission.query.get(admission_id):
        return jsonify({"error":"admission not found"}), 404
    bill_date = None
    if data.get('bill_date'):
        try:
            bill_date = datetime.fromisoformat(data['bill_date']).date()
        except Exception:
            return jsonify({"error":"bill_date must be ISO date"}), 400
    b = Bill(admission_id=admission_id, amount=amount, bill_date=bill_date or datetime.now().date(), status=data.get('status','Unpaid'))
    db.session.add(b)
    db.session.commit()
    return jsonify({"id": b.id}), 201

# Simple activity log endpoint (read-only for dev)
@app.route('/api/logs', methods=['GET'])
def get_logs():
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(100).all()
    return jsonify([{"id":l.id,"entity":l.entity,"entity_id":l.entity_id,"action":l.action,"details":l.details,"created_at":l.created_at.isoformat()} for l in logs])

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
