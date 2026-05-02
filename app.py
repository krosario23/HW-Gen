from flask import Flask, request, send_file, render_template
import pymupdf
import os
import uuid
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def create_packet(main_path, temp_path, names, output_path, extra_copies):
    main_doc = pymupdf.open(main_path)
    temp_doc = pymupdf.open(temp_path)

    for _ in range(0, extra_copies - 1):
        main_doc.insert_pdf(temp_doc)

    for name in names:
        temp_doc = pymupdf.open(temp_path)

        for page in temp_doc:
            text_instances = page.search_for("Name:")

            for rect in text_instances:
                # cover old text
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                
                # insert new text
                page.insert_text(rect.tl, f"Name: {name}", fontsize=12)

        # append modified copy
        main_doc.insert_pdf(temp_doc)
        temp_doc.close()

    main_doc.save(output_path)
    main_doc.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf_file = request.files["pdf"]
        names_text = request.form["names"]
        extra_copies = int(request.form["extra_copies"])
        
        print(extra_copies)

        names = [n.strip() for n in names_text.splitlines() if n.strip()]

        file_id = str(uuid.uuid4())
        template_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
        copy_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_copy.pdf")
        output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_output.pdf")

        pdf_file.save(template_path)
        shutil.copy(template_path, copy_path)

        create_packet(template_path, copy_path, names, output_path, extra_copies)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)