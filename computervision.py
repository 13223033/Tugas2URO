import cv2

# Membaca video
cap = cv2.VideoCapture('object_video.mp4')

# Setup untuk menyimpan video output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Mengonversi frame ke HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Rentang warna merah di HSV
    lower_red1 = (0, 120, 70)    # Rentang pertama untuk merah
    upper_red1 = (10, 255, 255)
    
    lower_red2 = (170, 120, 70)  # Rentang kedua untuk merah
    upper_red2 = (180, 255, 255)
    
    # Membuat mask untuk kedua rentang merah
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    
    # Gabungkan kedua mask menjadi satu
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Mencari kontur pada mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtering dan menggambar bounding box
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Menampilkan frame dengan bounding box
    cv2.imshow('Mendeteksi objek', frame)
    
    # Menyimpan frame ke video output
    out.write(frame)
    
    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
