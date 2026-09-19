# UPI QR Payment Splitter

> Split a larger UPI payment into multiple scannable QR codes, with every installment capped at ₹1,999.

A privacy-first Flask application that turns one larger UPI payment into a sequence of prefilled QR codes. Enter the recipient name, exact UPI ID, and total amount; the app calculates the installments and generates QR codes in memory.

## Features

- Smart splitting into ₹1,999-or-less installments
- Prefilled UPI deep links with recipient, amount, and INR currency
- QR images generated in memory with qrcode + Pillow
- Copyable UPI-link fallback
- Stateless processing with no database or payment history
- Server-side validation for name, UPI ID, and amount
- Responsive, mobile-friendly interface
- No frontend framework required

## Example

A ₹4,500 payment becomes:

    QR 01 → ₹1,999
    QR 02 → ₹1,999
    QR 03 → ₹502

Each QR is generated from a UPI payment URI containing the payee and installment amount.

## Tech stack

| Layer | Technology |
| --- | --- |
| Backend | Python 3.10+, Flask 3 |
| QR generation | qrcode + Pillow |
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Templates | Jinja2 |

## Project structure

    .
    ├── main.py
    ├── requirements.txt
    ├── templates/
    │   └── index.html
    ├── static/
    │   ├── style.css
    │   └── favicon.svg
    ├── .gitignore
    ├── CONTRIBUTING.md
    ├── SECURITY.md
    └── LICENSE

## Run locally

    git clone https://github.com/work-preet035/UPI-Splitter.git
    cd UPI-Splitter
    python -m venv .venv

Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

macOS/Linux:

    source .venv/bin/activate

Install and run:

    pip install -r requirements.txt
    python main.py

The app uses port 81 by default. Set PORT to use another port:

    PORT=5000 python main.py

## Limits

- Maximum installment: ₹1,999
- Maximum total request: ₹10,000

These values are defined in main.py.

## Privacy & payment safety

The app does not use persistent storage. Recipient details and generated QR images are handled for the current request only.

This application does not process payments or collect UPI PINs. Always verify the recipient UPI ID, recipient name, and amount in your UPI application before confirming a payment.

See SECURITY.md for security reporting guidance.

## UPI compatibility

The app generates a standard-style upi://pay URI using payee address (pa), payee name (pn), amount (am), and currency (cu). Exact behavior can vary between UPI applications, so users should verify the prefilled details before authorization.

## Roadmap

- QR download/share actions
- Automated unit and integration tests
- Docker support
- Health-check endpoint
- Optional configurable installment limits

## License

MIT License. See LICENSE.

Built with Python, Flask, and a privacy-first approach to simple UPI payment splitting.
