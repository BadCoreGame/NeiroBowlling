# NeiroBowlling
Система распознавания игры в боулинг по фотографиям <!-- Описание репозитория -->

<!--Структура файлов-->
## Структура файлов
| Название        | Описание                                                        |
|-----------------|-----------------------------------------------------------------|
| object.py          | Обнаружение объектов на изображении                             |
| best.pt         | Кастомная модель на базе YOLOv11                                |
| class.py        | Классификация изображения                                       |
| README.md       | Информация о репозитории                                        |
| run_commands.py | Настройка программной среды и работа со скриптами               |
| yolo11n-cls.pt  | Оригинальная модель YOLOv11 (не используется)                   |

# Список версий

## v1.0.4

### Добавлено или Изменено
- Изменено название файла app.py на object.py 
- Обновлась информация в README.md

### Удалено
- Файл debug.txt

## v1.0.3

### Добавлено или Изменено
- Исправилось определение изображён ли на фотографии боулинг
- Обновлась информация в README.md

## v1.0.2

### Добавлено или Изменено
- Обновлась информация в README.md
- Добавился файл class.py отвечающий за классификацию изображения

## v1.0.1

### Добавлено или Изменено
- Обновлась информация в README.md

### Удалено
- Файл requirements.txt содержащий библиотеки для YOLOv11
- Содержимое файла debug.txt

## v1.0.0

### Добавлено или Изменено
- Обновлась информация в README.md
- Добавлен app.py, best.pt, debug.txt, run_commands.py, yolo11n.pt
- Обновилась модель YOLOv5 -> YOLOv11