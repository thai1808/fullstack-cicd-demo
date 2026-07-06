import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from models import db, Note

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://notes_user:notes_pass@localhost:5432/notesdb"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Retry kết nối DB tối đa 10 lần (mỗi lần cách 3s) — tránh crash khi Postgres
    # chưa kịp sẵn sàng lúc container backend khởi động trước.
    with app.app_context():
        for attempt in range(1, 11):
            try:
                db.create_all()
                print("[startup] Kết nối database thành công.")
                break
            except OperationalError as e:
                print(f"[startup] DB chưa sẵn sàng (lần {attempt}/10): {e}")
                time.sleep(3)
        else:
            raise RuntimeError("Không thể kết nối database sau nhiều lần thử.")

    @app.route("/api/health")
    def health():
        return jsonify(status="ok")

    @app.route("/api/notes", methods=["GET"])
    def get_notes():
        notes = Note.query.order_by(Note.id.desc()).all()
        return jsonify([n.to_dict() for n in notes])

    @app.route("/api/notes", methods=["POST"])
    def add_note():
        data = request.get_json()
        content = (data or {}).get("content", "").strip()
        if not content:
            return jsonify(error="content is required"), 400
        note = Note(content=content)
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201

    @app.route("/api/notes/<int:note_id>", methods=["DELETE"])
    def delete_note(note_id):
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify(deleted=note_id)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
