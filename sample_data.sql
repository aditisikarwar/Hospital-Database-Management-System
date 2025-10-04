-- sample_data.sql
USE hospital_db;

-- Departments
INSERT INTO department (name, location) VALUES
('General Medicine', 'Block A'),
('Cardiology', 'Block B'),
('Orthopedics', 'Block C'),
('Pediatrics', 'Block D'),
('Emergency', 'Ground Floor');

-- Doctors
INSERT INTO doctor (name, department_id, qualification, phone, email) VALUES
('Dr. Neha Sharma', 1, 'MBBS, MD (General Medicine)', '9999000001', 'neha.sharma@example.com'),
('Dr. Rajiv Patel', 2, 'MBBS, DM (Cardiology)', '9999000002', 'rajiv.patel@example.com'),
('Dr. Amit Verma', 3, 'MBBS, MS (Orthopedics)', '9999000003', 'amit.verma@example.com');

-- Rooms
INSERT INTO room (room_number, type, is_available) VALUES
('G-101','General', TRUE),
('P-201','Private', TRUE),
('ICU-1','ICU', TRUE),
('OT-1','OT', TRUE);

-- Patients
INSERT INTO patient (name, dob, gender, phone, email, address) VALUES
('Aditi Sikarwar', '2003-03-10', 'Female', '9876500001', 'aditi.s@example.com', 'Guna, Madhya Pradesh'),
('Samir Kumar', '1999-11-05', 'Male', '9876500002', 'samir.k@example.com', 'Greater Noida'),
('Rita Singh', '1985-03-23', 'Female', '9876500003', 'rita.s@example.com', 'Durgapur');

-- Appointments
INSERT INTO appointment (patient_id, doctor_id, appt_datetime, reason, status) VALUES
(1, 1, '2025-05-20 10:00:00', 'Follow-up: database project check', 'Scheduled'),
(2, 2, '2025-05-21 11:30:00', 'Chest pain', 'Scheduled'),
(3, 3, '2025-05-22 09:00:00', 'Knee pain', 'Scheduled');

-- Admission & Bill (example)
INSERT INTO admission (patient_id, room_id, admit_date, discharge_date, reason) VALUES
(2, 3, '2025-05-21 12:00:00', NULL, 'Cardiac observation');

INSERT INTO bill (admission_id, amount, bill_date, status) VALUES
(LAST_INSERT_ID(), 15000.00, CURDATE(), 'Pending');

-- Activity log sample
INSERT INTO activity_log (entity, entity_id, action, details) VALUES
('patient', 1, 'created', 'Seed patient created');
