from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
from model import inference

@csrf_exempt
def predict_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Load the image from the request
        file = request.FILES['image']
        np_img = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Perform inference
        category, group = inference(img)

        return JsonResponse({
            'category': category,
            'group': group,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
