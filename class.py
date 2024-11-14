import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
from ultralytics import YOLO
import os

# Загрузка модели
try:
    model = YOLO("yolo11n-cls.pt")  # Оффициальная модель
    #model = YOLO("./best.pt")
    print("YOLOv11 модель загружена успешно.")
except Exception as e:
    print("Ошибка загрузки YOLOv11 модели:", e)

# Хранение загруженных файлов
loaded_images = []
gotov_image = {}

# Добавьте переменные для обработки кликов
click_count = 0
click_timer = None

# Функция для обработки изображения
def process_image():
    global loaded_images, gotov_image
    if not loaded_images:
        result_label.config(text="Пожалуйста, загрузите изображение.")
        return
    
    for file_path in loaded_images:
        # Загружаем и обрабатываем изображение
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            return
        img = Image.open(file_path)
        results = model(img)
        print(f"Изображение {file_path} обработано.")

        results_img_bgr = results[0].plot()  # BGR-order numpy array
        results_img = Image.fromarray(results_img_bgr[..., ::-1])  # RGB-order PIL image
        gotov_image[file_path] = results_img

    # # Загружаем и обрабатываем изображение
    # print("Обработка запущена.")
    # img = Image.open(process_image.file_path)
    # results = model(img)
    # print("Изображение обработано.")

    # Отображаем изображение
    # for i, r in enumerate(results):
    #     results_img_bgr = r.plot()  # BGR-order numpy array
    #     results_img = Image.fromarray(results_img_bgr[..., ::-1])  # RGB-order PIL image

    #     results_img = results_img.resize((400, 400))

    #     img_tk = ImageTk.PhotoImage(results_img)
    #     canvas.create_image(0, i * 400, anchor="nw", image=img_tk)
    #     canvas.image = img_tk
    #     print("Результаты отобразились.")
    
    top_result = results[0]  # Получаем самый вероятный класс
    class_index = top_result.probs.top1  # Индекс класса с наибольшей вероятностью
    confidence = top_result.probs.top1conf  # Вероятность класса с наибольшей вероятностью
    class_name = model.names[class_index]  # Имя класса

    # Проверяем, является ли изображение боулингом
    if class_name in ["Egyptian_cat"]:
        result_label.config(text=f"Обнаружен боулинг с точностью {confidence * 100:.2f}%")
        print(f"Обнаружен боулинг с точностью {confidence * 100:.2f}%")
    else:
        result_label.config(text="Боулинг не обнаружен")
        print(f"Боулинг не обнаружен, потому что {class_name} ({confidence * 100:.2f}%) не является 'Bowling'.")


def on_click(event):
    global click_count, click_timer

    click_count += 1

    if click_count == 1:
        click_timer = root.after(250, reset_click_count)  # Установите таймер на 250 мс
    elif click_count == 2:
        root.after_cancel(click_timer)  # Отмените таймер, если это двойной клик
        look_image(loaded_images[window_list.curselection()[0]])  # Обработайте двойной клик
        reset_click_count()

def reset_click_count():
    global click_count, click_timer
    click_count = 0
    if click_timer is not None:
        root.after_cancel(click_timer)
        click_timer = None

def look_image(file_path):
    if file_path in gotov_image:
        img = gotov_image[file_path]  # Используем обработанное изображение
        print(f"Результаты отобразились для {file_path}")
    else:
        img = Image.open(file_path)  # Показываем оригинальное изображение
        print(f"Результаты отобразились для {file_path}")

    img = img.resize((400, 400))  # Изменяем размер изображения на 400x400
    img_tk = ImageTk.PhotoImage(img)
    # Очищаем canvas перед отображением нового изображения
    canvas.delete(tk.ALL)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk  # Сохраняем ссылку на изображение

# Функция для загрузки изображения
def upload_images():
    global loaded_images, method_var

    global loaded_images
    if method_var.get() == "files":
        file_paths = filedialog.askopenfilenames(
            title="Выберите изображения.",
            filetypes=[("Images file", "*.jpg;*.jpeg;*.png")]
        )

        if file_paths:
            loaded_images = file_paths
    elif method_var.get() == "folder":
        folder_path = filedialog.askdirectory(title="Выберите папку с изображениями.")
        if folder_path:
            loaded_images = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png", ".ico", ".bmp", ".tif", ".pcx")):
                        loaded_images.append(os.path.join(root, file))  # Сохраняем полные пути к файлам

    print(f"Изображения загружены: {loaded_images}")
    if loaded_images:
        result_label.config(text="")
        window_list.delete(0, tk.END)  # Удаляем предыдущие элементы
        for file_path in loaded_images:
            file_name = os.path.basename(file_path)  # Получаем имя файла из пути
            window_list.insert(tk.END, file_name)

# Создаем основное окно
backg='#212121'  # Установка цвета фона
text_color = '#ffffff'  # Цвет текста
button_bg = '#212121'  # Цвет фона кнопок
button_fg = '#ffffff'  # Цвет текста кнопок

root = tk.Tk()
root.title("NeiroBowlling")
root.iconphoto(False, tk.PhotoImage(file="./icno.png"))

w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2  # середина экрана
h = h // 2
w = w - 350  # смещение от середины
h = h - 300
root.geometry(f'1000x700+{w}+{h}')
root.resizable(True, True)
root.configure(bg=backg)

# разметка окна -------------------------------

# правая сторона окна----
frame_right = tk.LabelFrame(width="500", bg=backg)
frame_right.pack(fill="y", side=tk.RIGHT)
# Создаем элементы интерфейса

canvas = tk.Canvas(frame_right, bg=backg, width="400", height="400")
canvas.pack(side=tk.TOP, pady="20", padx="50")

result_label= tk.Label(frame_right, text="", bg=backg, fg='white', font=("Helvetica", 15, "bold"))
result_label.pack(side=tk.BOTTOM, fill="both", expand=True)

# разделитель-----
divine_line= tk.Label(bg="#f0f0f0", width="0")
divine_line.pack(side=tk.RIGHT, fill="y")

# левая сторона окна
frame_left = tk.LabelFrame(bg=backg)
frame_left.pack(side=tk.LEFT, fill="both", expand=True)
# Создаем элементы интерфейса
name = tk.Frame(frame_left, bg=backg, height="60")
name.pack(side=tk.TOP, fill="x", ipady="5")
name_label = tk.Label(name, text="NeiroBowling", bg=backg, fg='white', font=("Helvetica", 23, "bold"))
name_label.pack(side=tk.LEFT, padx="7")

name_img= Image.open("./logo.png")
name_img.thumbnail((50, 50))
name_img_tk= ImageTk.PhotoImage(name_img)
name_img_label = tk.Label(name, image=name_img_tk, bg=backg)
name_img_label.image = name_img_tk
name_img_label.pack(side=tk.LEFT)


explorer = tk.Frame(frame_left, bg=backg)
explorer.pack(side=tk.TOP, fill="both", expand=True)
window_list = tk.Listbox(explorer, bg=backg, fg="white")
window_list.pack(side=tk.LEFT, fill="both", expand=True)
window_list.bind("<Button-1>", on_click)
spisok = tk.Scrollbar(explorer, orient="vertical", command=window_list.yview)
spisok.pack(side=tk.RIGHT, fill="y")
window_list.config(yscrollcommand=spisok.set)
images_frame = tk.Frame(frame_left, bg=backg)
images_frame.pack(side=tk.TOP, fill="both", expand=True)



# Кнопка обработки изображений
process_button = tk.Button(frame_left, text="Обработать изображения", command=process_image, bg=button_bg, fg=button_fg, font=("Helvetica", 12, "bold"))
process_button.pack(side=tk.BOTTOM, pady=10)

# Переменные для радиокнопок
method_var = tk.StringVar(value="files")  # Значение по умолчанию - загрузка файлов

    # Радиокнопки для выбора метода загрузки
select_frame = tk.LabelFrame(frame_left, bg=backg, text="select", fg="white")
select_frame.pack(side=tk.BOTTOM, fill="x", pady="10", padx="30")
tk.Radiobutton(select_frame, text="Загрузить файлы", variable=method_var, value="files", bg=backg, fg=button_fg, font=("Helvetica", 12, "bold"), selectcolor=button_bg).pack(anchor=tk.SW, pady="5", padx="5")
tk.Radiobutton(select_frame, text="Загрузить папку", variable=method_var, value="folder", bg=backg, fg=button_fg, font=("Helvetica", 12, "bold"), selectcolor=button_bg).pack(anchor=tk.SW, pady="5", padx="5")

# Кнопка загрузки изображений
upload_button = tk.Button(frame_left, text="Загрузить изображения", command=upload_images, bg=button_bg, fg=button_fg, font=("Helvetica", 12, "bold"))
upload_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
