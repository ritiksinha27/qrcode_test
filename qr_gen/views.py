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

        img = qr.make_image(fill_color='black', back_color='white')

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


# for qr code scanner
import cv2
from PIL import Image
import numpy as np
from django.shortcuts import render
from .forms import QRCodeUploadForm

def scan_qr_image(request):
    if request.method == 'POST':
        form = QRCodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            print(image)
            # Convert the uploaded image to OpenCV format
            img = Image.open(image)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            qr_code_detector = cv2.QRCodeDetector()
            data, bbox, _ = qr_code_detector.detectAndDecode(img)
            print(data, 'data'), print(bbox,'bbox')
            if bbox is not None and data:
                user_data = {}
                for item in data.split(';'):
                    # Ensure the item can be split into two parts
                    if ':' in item:
                        key, value = item.split(':', 1)  # Split into at most 2 parts
                        user_data[key] = value
                return render(request, 'qr_detail.html', {'data': data})
            else:
                return render(request, 'qr_scan.html', {'form': form, 'error': 'No QR code found'})
    else:
        form = QRCodeUploadForm()
    return render(request, 'qr_scan.html', {'form': form})

# import cv2
# from django.http import StreamingHttpResponse, HttpResponseRedirect
# from django.shortcuts import render
# from django.urls import reverse
# import webbrowser

# def generate_camera_stream():
#     cap = cv2.VideoCapture(0)
#     detector = cv2.QRCodeDetector()
#     while True: 
#         _,img=cap.read()
#         data,one,_=detector.detectAndDecode(img)
#         if data :
#             a=data
#             break
#         cv2.imshow("qrcode",img)
#         if cv2.waitKey(1) ==ord('q'):
#             break
#     b=webbrowser.open(str(a))
#     cap.release(a)
#     cv2.destroyAllWindows()
    
import cv2
import webbrowser
from django.http import StreamingHttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import quote

detected_data = None
'''
def generate_camera_stream(detected_data_container):
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, img = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            detected_data_container['data'] = data
            print(detected_data_container)
            break

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()
    cv2.destroyAllWindows()
    

def scan_qr_live(request):
    if 'detected_data' in request.session:
        data = request.session.pop('detected_data')
        print(f"Redirecting to process_qr_data with data: {data}")
        return HttpResponseRedirect(reverse('process_qr_data') + f'?data={data}')
    return render(request, 'scan_qr_live.html')

def live_camera(request):
    detected_data_container = {}
    response = StreamingHttpResponse(generate_camera_stream(detected_data_container),
                                     content_type='multipart/x-mixed-replace; boundary=frame')
    if 'data' in detected_data_container:
        request.session['detected_data'] = detected_data_container['data']
        print(f"Detected data set in session: {detected_data_container['data']}")
    return response

def check_qr_data(request):
    global detected_data_container
    if 'data' in detected_data_container:
        data = detected_data_container.pop('data')
        return JsonResponse({'detected': True, 'data': data})
    return JsonResponse({'detected': False})

def process_qr_data(request):
    detected_data = request.GET.get('data', '')
    user_data = {}
    for item in detected_data.split(';'):
        if ':' in item:
            key, value = item.split(':', 1)  # Split into at most 2 parts
            user_data[key] = value
    return render(request, 'qr_detail.html', {'data': user_data})'''
    
detected_data_container = {}

def generate_camera_stream():
    global detected_data_container
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, img = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            detected_data_container['data'] = data
            break

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()
    cv2.destroyAllWindows()

def scan_qr_live(request):
    return render(request, 'scan_qr_live.html')

def live_camera(request):
    return StreamingHttpResponse(generate_camera_stream(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def check_qr_data(request):
    global detected_data_container
    if 'data' in detected_data_container:
        data = detected_data_container.pop('data')
        print(f"QR Data Detected: {data}")
        request.session['user']=data
        return JsonResponse({'detected': True, 'data': data})
    print("No QR Data Detected")
    return JsonResponse({'detected': False})

def process_qr_data(request):
    usr=request.session.get('user')
    
    return render(request, 'qr_detail.html', {'data': usr})