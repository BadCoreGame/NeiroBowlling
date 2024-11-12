import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
from ultralytics import YOLO

# Загрузка модели
#model = YOLO("yolo11n.pt")  # Оффициальная модель
try:
    model = YOLO("./best.pt")  # load a custom model
    print("YOLOv11 модель загружена успешно.")
except Exception as e:
    print("Ошибка загрузки YOLOv11 модели:", e)

# Функция для обработки изображения
def process_image():
    if not hasattr(process_image, 'file_path') or not process_image.file_path:
        result_label.config(text="Пожалуйста, загрузите изображение.")
        return

    # Загружаем и обрабатываем изображение
    img = Image.open(process_image.file_path)
    results = model(img)
    print("Изображение обработано.")

    # Отображаем изображение с выделенными объектами
    for i, r in enumerate(results):
        results_img_bgr = r.plot()  # BGR-order numpy array
        results_img = Image.fromarray(results_img_bgr[..., ::-1])  # RGB-order PIL image
        results_img = results_img.resize((400, 400))

        #print(f"results{i}.jpg") # Выводит название обработанного файла и его нумерацию в массиве

    #results_img = Image.fromarray(results_img)
    #results_img = results_img.resize((400, 400))
    img_tk = ImageTk.PhotoImage(results_img)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk
    print("Результаты отобразились.")

    # Проверяем, обнаружены ли объекты, похожие на боулинг
    labels = r.boxes.cls  # Классы объектов
    confidences = r.boxes.conf  # Вероятности объектов
    class_names = model.names  # Получаем имена классов из модели

    bowling_detected = False
    max_confidence = 0.0
    for label, confidence in zip(labels, confidences):
        if class_names[int(label)] in ["bowling-ball", "bowling-pins"]:
            bowling_detected = True
            max_confidence = max(max_confidence, confidence)

    # Обновляем результат
    if bowling_detected:
        result_label.config(text=f"Обнаружен боулинг с точностью {max_confidence * 100:.2f}%")
        print(f"Обнаружен боулинг с точностью {max_confidence * 100:.2f}%")
    else:
        result_label.config(text="Боулинг не обнаружен")
        print("Боулинг не обнаружен.")

# Функция для загрузки изображения
def load_image():
    process_image.file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
    )
    print("Изображение загружено.")
    if process_image.file_path:
        img = Image.open(process_image.file_path)
        img = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk
        result_label.config(text="")

# Создаем основное окно
root = tk.Tk()
root.title("Bowling Detector")
root.geometry("500x600")
root.resizable(False, False)

# Кнопка загрузки изображения
load_button = tk.Button(root, text="Загрузить изображение", command=load_image, font=("Arial", 14), bg="lightblue")
load_button.pack(pady=10)

# Поле для отображения изображения
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Кнопка обработки изображения
process_button = tk.Button(root, text="Обработать", command=process_image, font=("Arial", 14), bg="lightgreen")
process_button.pack(pady=10)

# Метка для отображения результата
result_label = tk.Label(root, text="", font=("Arial", 14), fg="black")
result_label.pack(pady=10)

root.mainloop()
