import cv2
import torch
import time
from config import DefaultConfig
from models.mobilenetv3 import MobileNetV3_Small
from torchvision import transforms

def cvImgToTensor(cvImg):
    image = cvImg.copy()
    height, width, channel = image.shape
    ratio = 224 / min(height, width)
    image = cv2.resize(image, None, fx=ratio, fy=ratio)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    if image is not None:
        image = image[:, :, (2, 1, 0)]
        image = transform(image)
        image.unsqueeze_(0)

    return image

# Load dataset info
DataSetInfo = torch.load(DefaultConfig.DataSetInfoPath)
index_to_class = DataSetInfo['index_to_class']
index_to_group = DataSetInfo['index_to_group']

# Load model
MyModel = MobileNetV3_Small(DataSetInfo["class_num"])
device = torch.device('cuda') if DefaultConfig.InferWithGPU else torch.device('cpu')
MyModel.load_state_dict(torch.load(DefaultConfig.CkptPath, map_location=torch.device('cpu'))['state_dict'])
MyModel.to(device)
MyModel.eval()

def inference(cvImg):
    image = cvImgToTensor(cvImg)
    image = image.to(device)
    with torch.no_grad():
        result = MyModel(image)
    _, predicted = torch.max(result, 1)
    predicted = predicted.item()
    return index_to_class[predicted], index_to_group[predicted]

def main():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if ret:
            t0 = time.time()
            category, group = inference(frame)
            t1 = time.time()

            cv2.putText(frame, f'Category: {category}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Group: {group}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Inference time: {t1-t0:.2f}s', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Garbage Classification', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()