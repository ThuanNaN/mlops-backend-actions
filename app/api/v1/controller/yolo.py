

def yolo_prediction(model, image):
    results = model(image)

    detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Extract detection information
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            bbox = box.xyxy[0].tolist()
            
            detections.append({
                'class': model.names[cls],
                'confidence': conf,
                'bounding_box': {
                    'x1': bbox[0],
                    'y1': bbox[1],
                    'x2': bbox[2],
                    'y2': bbox[3]
                }
            })

    return detections