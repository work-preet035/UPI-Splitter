import base64
import os
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from io import BytesIO
from urllib.parse import urlencode

import qrcode
from flask import Flask, render_template, request

app = Flask(__name__)
MAX_TRANSACTION = Decimal("1999")
MAX_TOTAL = Decimal("10000")
TWO_PLACES = Decimal("0.01")

def format_inr(value: Decimal) -> str:
    normalized = value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
    if normalized == normalized.to_integral():
        return f"{normalized:,.0f}"
    return f"{normalized:,.2f}".rstrip("0").rstrip(".")

def format_upi_amount(value: Decimal) -> str:
    normalized = value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
    return format(normalized, "f").rstrip("0").rstrip(".")

def split_amount(total: Decimal) -> list[Decimal]:
    chunks = []
    remaining = total
    while remaining > 0:
        chunk = min(remaining, MAX_TRANSACTION)
        chunks.append(chunk)
        remaining -= chunk
    return chunks

def qr_as_data_uri(payload: str) -> str:
    image = qrcode.make(payload)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"

def build_qr_items(name: str, upi_id: str, chunks: list[Decimal]) -> list[dict]:
    items = []
    for index, chunk in enumerate(chunks, start=1):
        amount_label = format_inr(chunk)
        upi_amount = format_upi_amount(chunk)
        link = "upi://pay?" + urlencode({"pa": upi_id, "pn": name, "am": upi_amount, "cu": "INR"})
        items.append({"number": index, "amount": chunk, "amount_label": amount_label, "link": link, "image": qr_as_data_uri(link)})
    return items

@app.template_filter("inr")
def inr_filter(value: Decimal) -> str:
    return format_inr(value)

@app.route("/", methods=["GET", "POST"])
def home():
    form = {"name": "", "upi_id": "", "amount": ""}
    errors = []
    qr_items = []
    total = None
    if request.method == "POST":
        form = {"name": request.form.get("name", "").strip(), "upi_id": request.form.get("upi_id", "").strip(), "amount": request.form.get("amount", "").strip()}
        if not form["name"]:
            errors.append("Enter the recipient's name.")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+", form["upi_id"]):
            errors.append("Enter a valid UPI ID, for example name@bank.")
        try:
            total = Decimal(form["amount"]).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError):
            total = None
        if total is None or total <= 0:
            errors.append("Enter an amount greater than ₹0.")
        elif total > MAX_TOTAL:
            errors.append("The maximum amount is ₹10,000.")
        if not errors and total is not None:
            qr_items = build_qr_items(form["name"], form["upi_id"], split_amount(total))
    return render_template("index.html", form=form, errors=errors, qr_items=qr_items, total=total)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "81"))
    app.run(host="0.0.0.0", port=port, debug=False)
