import cv2


def VideoProcess(path):
    cap = cv2.VideoCapture(path)
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter("static/media/"+'output.mp4', -1,
                          20.0, (frame_width, frame_height))
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            canny = cv2.Canny(blur, 10, 70)
            ret, mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
            out.write(mask)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    PATH = "/static/media/"+'output.mp4'
    return PATH
