import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO

# Загрузка модели
try:
    model = YOLO("./best.pt")  # load a custom model
    print("YOLOv11 модель загружена успешно.")
except Exception as e:
    print("Ошибка загрузки YOLOv11 модели:", e)

# Хранение загруженных файлов 
loaded_images = []
gotov_image = {}

def process_image():
    global loaded_images, gotov_image
    if not loaded_images:
        result_label.config(text="Пожалуйста, загрузите изображение.")
        return
        
    for file_path in loaded_images:
        # Загружаем и обрабатываем изображение
        img = Image.open(file_path)
        results = model(img)
        print(f"Изображение {file_path} обработано.")
        gotov_image[file_path] = results

        # Отображаем изображение с выделенными объектами
        for i, r in enumerate(results):
            results_img_bgr = r.plot()  # BGR-order numpy array
            results_img = Image.fromarray(results_img_bgr[..., ::-1])  # RGB-order PIL image
            
            results_img = results_img.resize((400, 400))

            img_tk = ImageTk.PhotoImage(results_img)
            canvas.create_image(0, i * 400, anchor="nw", image=img_tk)
            canvas.image = img_tk

            labels = r.boxes.cls
            confidences = r.boxes.conf  # Вероятности объектов
            class_names = model.names  # Получаем имена классов

            bowling_detected = False
            max_confidence = 0.0
            for label, confidence in zip(labels, confidences):
                if class_names[int(label)] in ["bowling-ball", "bowling-pins"]:
                    bowling_detected = True
                    max_confidence = max(max_confidence, confidence)
            if bowling_detected:
                result_label.config(text=f"Обнаружен боулинг на изображении {file_path} с точностью {max_confidence * 100:.2f}%")
                print(f"Обнаружен боулинг на изображении {file_path} с точностью {max_confidence * 100:.2f}%")
            else:
                result_label.config(text=f"Боулинг не обнаружен на изображении {file_path}")
                print(f"Боулинг не обнаружен на изображении {file_path}.")

# Функция для загрузки изображений из массива
def display_loaded_images():
    for widget in images_frame.winfo_children():
        widget.destroy()  # Удаляем предыдущие элементы
    
    for file_path in loaded_images:
        file_name = file_path.split("/")[-1]  # Получаем имя файла из пути
        img = Image.open(file_path)
        img.thumbnail((100, 100))  # Уменьшаем изображение для отображения в списке
        img_tk = ImageTk.PhotoImage(img)
        
        # Создаем метку для имени файла
        name_label = tk.Label(images_frame, text=file_name, bg='white', fg='black')
        name_label.pack(side=tk.TOP)

        # Создаем метку для изображения
        img_label = tk.Label(images_frame, image=img_tk, bg='white')
        img_label.image = img_tk  # Сохраняем ссылку на изображение
        img_label.pack(side=tk.TOP)

# Функция для загрузки изображений
def upload_images():
    """Upload images and display them."""
    global loaded_images
    file_paths = filedialog.askopenfilenames(title="Выберите изображения.",
    
    filetypes=[("Images file", "*.jpg;*.jpeg;*.png;*.ico;*.bmp;*.tif;*.pcx;*")])  # Выбор файлов
    
    loaded_images = file_paths
    print(f"Изображения загружены: {loaded_images}")
    if loaded_images:
        result_label.config(text="")
        display_loaded_images()

# Создаем основное окно -------------
backg='#222831'  # Установка цвета фона
root = tk.Tk()
root.title("NeiroBowling")

w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2  # середина экрана
h = h // 2
w = w - 500  # смещение от середины
h = h - 300

root.geometry(f'1000x600+{w}+{h}')
root.resizable(False, False)
root.configure(bg=backg)

# Создаем элементы интерфейса
images_frame = tk.Frame(root, bg=backg)
images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(root, bg=backg, width=500, height=600)
canvas.pack(side=tk.RIGHT)

result_label = tk.Label(root, text="", bg=backg, fg='white')
result_label.pack(side=tk.BOTTOM)

# Кнопка загрузки изображений
upload_button = tk.Button(root, text="Загрузить изображения", command=upload_images)
upload_button.pack(side=tk.BOTTOM)

# Кнопка обработки изображений
process_button = tk.Button(root, text="Обработать изображения", command=process_image)
process_button.pack(side=tk.BOTTOM)

root.mainloop()
