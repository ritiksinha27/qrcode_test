import qrcode
from django.http import HttpResponse
from django.shortcuts import render

def generate_qr1(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        img = qrcode.make(data)
        
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    return render(request, 'qr_code.html')

def generate_qr(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        qr = qrcode.QRCode(
            version=8,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color='white', back_color='red')

        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    return render(request, 'qr_code.html')

# for using the image in the middle of qr code:from PIL import Image

# def generate_qr(request):
#     if request.method == 'POST':
#         data = request.POST.get('data')
        
#         # Create a QR Code instance
#         qr = qrcode.QRCode(
#             version=None,  # Automatically determine the smallest version
#             error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction level to accommodate the logo
#             box_size=10,
#             border=4,
#         )
        
#         # Add data to the QR Code
#         qr.add_data(data)
#         qr.make(fit=True)
        
#         # Create an image from the QR Code instance
#         img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

#         # Open the logo image
#         logo = Image.open('path/to/logo.png')
        
#         # Calculate the size of the logo
#         logo_size = min(img.size) // 3  # Logo size as one third of the QR code's smallest dimension
#         logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

#         # Calculate the position to paste the logo (center)
#         logo_position = (
#             (img.size[0] - logo_size) // 2,
#             (img.size[1] - logo_size) // 2,
#         )

#         # Paste the logo onto the QR code
#         img.paste(logo, logo_position, mask=logo)

#         # Prepare HTTP response with the QR code image
#         response = HttpResponse(content_type="image/png")
#         img.save(response, "PNG")
#         return response
#     return render(request, 'qrapp/generate_qr.html')

    