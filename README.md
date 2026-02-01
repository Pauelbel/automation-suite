#### Введение
Швейцарский нож автоматизированного тестирования. :) 

### Начало работы 
- `py -m venv .venv` (для создания виртуального окружения)

#### Установка из requirements.txt:
-  `pip install -r requirements.txt`

#### Выборочная установка (оптимальна при ризделении на отдельные репозитории):

| Общие                     | Для UI                        | Для API                  | Для скриншотного          |
| ------------------------- | ----------------------------- | ------------------------ | ------------------------- |
| pip install pytest        | pip install pytest-playwright | pip install zeep  (soap) | pip install numpy         |
| pip install allure-pytest | playwright install            | pip install pydantic     | pip install opencv-python |

#### Конфигурации
- Переименовать `.credentials Example` в `.credentials` (в качестве примера уже запонен данными)
