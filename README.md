HW-Gen is a web app that generates personalized PDF homework packets for a list of students.
Here's how it works:

1. You upload a PDF template — a homework sheet that has a "Name:" field somewhere on it.
2. You provide a list of student names — entered as text, one per line.
3. The app generates one copy of the PDF per student, automatically replacing the "Name:" placeholder with each student's actual name.
4. It bundles all the copies into a single PDF and sends it back to you as a download.

Tech stack: It's a Python Flask web app using pymupdf (also known as PyMuPDF/fitz) to manipulate the PDFs — specifically to find the "Name:" text on each page, white it out, and overwrite it with the student's name.
Practical use case: A teacher could upload a blank homework sheet, paste in a class roster, and instantly get a ready-to-print PDF with every student's name already filled in — no manual copy-pasting needed.

README written by Claude
