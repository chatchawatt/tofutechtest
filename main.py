from fastapi import FastAPI, Request, HTTPException, File, UploadFile
from fastapi.responses import Response,JSONResponse
# from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF4 import PdfFileWriter,PdfFileReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


from pydantic import BaseModel
import sqlite3,io

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

conn = sqlite3.connect('applicants.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS applicants
             (id INTEGER PRIMARY KEY AUTOINCREMENT , first_name TEXT, last_name TEXT, phone TEXT, address TEXT, expected_salary REAL)''')
conn.commit()


class User(BaseModel):
    username: str
    password: str

class ApplicantCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    address: str
    expected_salary: float
class Applicant(ApplicantCreate):
    id:int

fake_users = {
    "user1": {
        "password": "password1"
    }
}    

@app.post("/login")
async def pos_login(user: User):
    if user.username in fake_users and user.password == fake_users[user.username]["password"]:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


@app.post("/submit_application")
async def submit_application(applicant: ApplicantCreate):
    c.execute('''INSERT INTO applicants (first_name,last_name,phone, address, expected_salary) VALUES (?, ?, ?, ?, ?)''',
              (applicant.first_name, applicant.last_name, applicant.phone, applicant.address, applicant.expected_salary))
    conn.commit()
    return {"message": "Application submitted successfully"}

@app.get("/applicants")
async def get_applicants():
    
    conn = sqlite3.connect('applicants.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM applicants''')
    rows = cursor.fetchall()
    applicants = []
    for row in rows:
        applicants.append(Applicant(id=row[0],first_name=row[1], last_name=row[2],phone=row[3], address=row[4], expected_salary=row[5]))
    conn.close()
    return applicants

@app.put("/applicants/{applicant_id}")
async def update_applicant(applicant_id: int, applicant: ApplicantCreate):
    c.execute('''UPDATE applicants SET first_name=?, last_name=?, phone=?, address=?, expected_salary=?
              WHERE id=?''', (applicant.first_name, applicant.last_name, applicant.phone, applicant.address, applicant.expected_salary, applicant_id))
    conn.commit()
    return {"message": "Applicant updated successfully"}


@app.delete("/applicants/{applicant_id}")
async def delete_applicant(applicant_id: int):
    conn = sqlite3.connect('applicants.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM applicants WHERE id = ?''', (applicant_id,))
    conn.commit()
    conn.close()
    return {"message": "Applicant deleted successfully"}

@app.get("/export")
async def get_export():

    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM applicants''')
    rows = cursor.fetchall()

    buffer = io.BytesIO()

    
    doc = SimpleDocTemplate(buffer,pagesize=letter)
    td = [["ID","FIRST NAME", "LAST NAME", "PHONE", "ADDRESS", "EXPECTED SALARY"]]
    for row in rows:
        td.append([str(value) for value in row])

    table = Table(td)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'gray'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), 'beige'),
        ('GRID', (0, 0), (-1, -1), 1, 'black')
    ])
    table.setStyle(style)

    elements = [table]   
    doc.build(elements)
    buffer.seek(0)
    
    headers = {'Content-Disposition': 'attachment; filename="out.pdf"'}
    return Response(content=buffer.getvalue(), headers=headers, media_type='application/pdf')

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        reader = PdfFileReader(file.file)
        data = []
        cursor = conn.cursor()
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            data.append(page.extractText())
            lines = data[0].split("\n\n")
            lines = lines[6:]
            while len(lines)>=6:
                first_name = lines[1]
                last_name = lines[2]
                phone = lines[3]
                address = lines[4]
                expected_salary = float(lines[5])

                cursor.execute("SELECT id FROM applicants WHERE first_name = ? AND last_name = ?", (first_name, last_name))
                existing_applicant = cursor.fetchone()
                if existing_applicant:
                    cursor.execute('''UPDATE applicants SET phone=?, address=?, expected_salary=?
                                      WHERE id=?''', (phone, address, expected_salary, existing_applicant[0]))
                else:
                    cursor.execute('''INSERT INTO applicants (first_name, last_name, phone, address, expected_salary)
                                      VALUES (?, ?, ?, ?, ?)''', (first_name, last_name, phone, address, expected_salary))
                lines = lines[6:]
        
        conn.commit()

        return JSONResponse(content={"message": "PDF uploaded successfully."})
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)
    
@app.get("/")
async def get_root():
    return FileResponse("dist/index.html")
app.mount("/", StaticFiles(directory="dist", html=True))





