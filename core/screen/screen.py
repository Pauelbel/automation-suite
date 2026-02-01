import cv2
import numpy as np

# Настройки
indent = 5              # Отступ вокруг контуров
rgb = (204, 0, 204)     # Цвет обводки (BGR)
thickness = 2           # Толщина рамки
fill_alpha = 0.3        # Прозрачность заливки
threshold = 0.01        # Порог различий

img1 = "/media/pv_belov/Жесткий/repo/automation-suite/tests/screen/1.png"
img2 = "/media/pv_belov/Жесткий/repo/automation-suite/tests/screen/2.png"

def compare_images(baseline_path, current_path, threshold=0.01):
    # Загружаем изображения
    base = cv2.imread(baseline_path)
    curr = cv2.imread(current_path)

    if base is None:
        raise FileNotFoundError(f"Исходное изображение не найдено: {baseline_path}")
    if curr is None:
        raise FileNotFoundError(f"Текущее изображение не найдено: {current_path}")
    if base.shape != curr.shape:
        raise ValueError("Размер изображений различается")

    # Абсолютная разница
    diff = cv2.absdiff(base, curr)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

    # Доля изменённых пикселей
    diff_ratio = np.count_nonzero(mask) / mask.size

    # Копия изображения для выделения различий
    highlight = base.copy()

    # Контуры различий
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    overlay = highlight.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x1 = max(x - indent, 0)
        y1 = max(y - indent, 0)
        x2 = min(x + w + indent, base.shape[1] - 1)
        y2 = min(y + h + indent, base.shape[0] - 1)
        
        # Рамка
        cv2.rectangle(highlight, (x1, y1), (x2, y2), rgb, thickness)
        # Полупрозрачная заливка
        cv2.rectangle(overlay, (x1, y1), (x2, y2), rgb, -1)

    # Смешиваем overlay с highlight
    cv2.addWeighted(overlay, fill_alpha, highlight, 1 - fill_alpha, 0, highlight)

    return diff_ratio, highlight

def test_visual_regression():
    diff_ratio, highlight = compare_images(img1, img2, threshold=threshold)

    # Сохраняем результат сразу
    cv2.imwrite("tests/highlight.png", highlight)

    print(f"Процент визуальной разницы: {diff_ratio*100:.2f}%")
    assert diff_ratio < threshold, f"Слишком большая визуальная разница: {diff_ratio:.4f}"

test_visual_regression()



12