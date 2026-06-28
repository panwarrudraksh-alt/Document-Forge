import base64
with open("static/upi_qr.jpeg", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")
    print(f"data:image/jpeg;base64,{encoded}")
