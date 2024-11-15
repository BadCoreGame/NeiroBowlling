# библиотеки -----------------------------
import os # работа с файлами и директориями
import tkinter as tk #для создания окна
from tkinter import filedialog, messagebox # tkinter импорт
import customtkinter as ctk #tkinter модуль красоты
from PIL import Image, ImageTk #tkinter оьраьотка для него изображений
import pandas as pd #для создания xlsx файла
#   
    # классы прикольная тема, т.к. переменные и функции вызываются так-же, но с припиской в начале:
    # Пример: peremens.переменная = 5 или functions.функция()


# дальше функции --------------------------
class peremens():# глобальные переменные
    Path_dir="" #путь к папке
    loaded_images_paths = [] # загруженные пути к картинкам


class Functions():# функции tkinter
    def log(name): # логирование
        print(name)
        names = "  "+ name
        dev_log.configure(state="normal") 
        dev_log.insert(tk.END,names)# логирование
        dev_log.configure(state="disabled")
    
    def download_images(): # загрузка папки
        peremens.Path_dir= filedialog.askdirectory(title="Выберите папку с изображениями.") # выбор папки
        Functions.log(f"Загружен каталог {peremens.Path_dir}")
        if peremens.Path_dir: # проверка на пустоту пути
            peremens.loaded_images_paths = [] #очистка списка
            # дальше поиск файлов по директориям и запись полного пути
            for root, dirs, files in os.walk(peremens.Path_dir):
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png", ".ico", ".bmp", ".tif", ".pcx")):
                        peremens.loaded_images_paths.append(os.path.join(root, file))
        print(f"Изображения загружены: {peremens.loaded_images_paths}")
    
    def start():# старт обработки фотографий
        if not peremens.loaded_images_paths:
            messagebox.showwarning("Не торопитесь", "Пожалуйста, загрузите изображение.")
            return
        neironka.pizdec()# вызов функции нейро пизды
        Functions.save_result()# вызов функции сохранения в xlsx файл
        print("start")

    def save_result(): #сохранение результата
        # функция сохранения результата в xlsx файле
        def create_empty_excel(columns: list, filename: str, sheet_name: str = 'Sheet1'):
            df = pd.DataFrame(columns=columns)

            if not os.path.exists('excel_files'):
                os.makedirs('excel_files')

            filepath = os.path.join('excel_files', filename)
            excel_writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
            df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
            excel_writer._save()

            return filepath
        
        create_empty_excel(columns=['Имя', 'Адрес', 'Email', 'Телефон'], filename='resultats.xlsx')
        
        print("save_result")

class neironka(): # функции для общения с нейронкой
    def pizdec():
        print("pizdec")

## Создание окна ------------------------------------
root_window = ctk.CTk() # создаем окно
def create_window(): # настройка окна
    # функция для создания окна
    root_window.title("NeiroBowling") # название окна
    h = root_window.winfo_screenheight() # высота экрана рабочего стола
    w = root_window.winfo_screenwidth() # ширина экрана рабочего стола
    hr=450# высота окна
    wr=400# ширина окна
    root_window.geometry(f"{wr}x{hr}+{w//2-wr//2}+{h//2-hr//2}") # задаем размеры окна и отступ
    root_window.resizable(False, False) # разрешаем изменять размеры окна
    root_window.wm_iconbitmap() 
    root_window.iconphoto(False, ImageTk.PhotoImage(file=".\\icon.png")) 
create_window()

def create_logo(): # название и лого
    frame_logo = ctk.CTkFrame(root_window, fg_color="transparent")
    frame_logo.pack(side=tk.TOP, fill="x", expand=False, pady=20)
    
    frame_logo_na = ctk.CTkFrame(frame_logo, fg_color="transparent")
    frame_logo_na.pack(anchor=tk.CENTER)
    
    ctk.CTkLabel(frame_logo_na, text="NeiroBowling", font=ctk.CTkFont("Helvetica", size=40, weight="bold")).pack(side=tk.LEFT,pady=0)# размещение

    logo = ctk.CTkImage(Image.open(".\\logo.png"), size=(80, 80)) # загрузка логот
    ctk.CTkLabel(frame_logo_na, image=logo, text="").pack(side=tk.LEFT, pady=10) # размещение логотип
create_logo()

tabview = ctk.CTkTabview(master=root_window, corner_radius=25) # создание перекюлчателя страничек
tabview.pack(side=tk.BOTTOM, fill="both", expand=True, padx=30, pady=30) # размещение переключателя

def create_tab_single_mode(): # создание странички для одиночных папок
    tabview.add("neiro") # добавление таба

    def upload_button(): # кнопка для выбора папки с файлами
        Button_explorer = ctk.CTkButton(master=tabview.tab("neiro"), text="Выбрать папку", command=Functions.download_images, font=ctk.CTkFont("Helvetica", size=18, weight="bold"), corner_radius=20, height=40) # создание кнопки для выбора папки c файлами
        Button_explorer.pack(side=tk.TOP, padx=5, pady=20, fill="x") # размещение кнопки для выбора папки c файлами  
    upload_button()

    def run_button(): # кнопка для запуска обработки
        Button_explorer = ctk.CTkButton(master=tabview.tab("neiro"), text="Обработать Изображение", command=Functions.save_result, font=ctk.CTkFont("Helvetica", size=18, weight="bold"), corner_radius=20, height=40,) # создание кнопки для выбора папки c файлами
        Button_explorer.pack(side=tk.TOP, padx=5, pady=20, fill="x") # размещение кнопки для выбора папки c файлами 
    run_button()
create_tab_single_mode()

# логирование в массив не ложить
tabview.add("devtool") # добавление таба
dev_log = ctk.CTkTextbox(tabview.tab("devtool"), state="disable")  # изменено на "normal"
def create_textbox(): #создание поля логирования
    # текстовое пространство для логирование
    dev_log.pack(padx=0, pady=0, fill="both")
    # создание для него scrollbar
    scrollbar = ctk.CTkScrollbar(tabview.tab("devtool"), command=dev_log.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
 
    # связываем scrollbar с текстовым полем
    dev_log.configure(yscrollcommand=scrollbar.set)

    # Пример добавления текста в dev_log
    Functions.log("Логирование запущено...\n")
create_textbox()

# запуск окна
root_window.mainloop()