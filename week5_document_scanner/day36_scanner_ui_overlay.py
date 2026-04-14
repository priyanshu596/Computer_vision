import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('../outputs', exist_ok=True)

# ─────────────────────────────────────────────
# TEST IMAGE
# ─────────────────────────────────────────────
def make_test_document():
    canvas = np.ones((500, 600, 3), dtype=np.uint8) * 120
    pts = np.array([[80, 60], [520, 30], [540, 440], [60, 460]], dtype=np.int32)
    cv2.fillPoly(canvas, [pts], (240, 240, 230))
    for y in range(100, 420, 35):
        cv2.line(canvas, (100, y), (500, y - 10), (180, 180, 180), 1)
    return canvas, pts

#img, doc_pts = make_test_document()
img=cv2.imread("document1.webp")

# ─────────────────────────────────────────────
# STEP 1 — Detect document corners
# ─────────────────────────────────────────────
def find_document_corners(img):
    """Returns 4 corner points of the largest quadrilateral, or None."""
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 100, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    doc_contours = []
    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)

        if len(approx) == 4 and area > 5000:
            doc_contours.append(approx)

    if len(doc_contours) == 0:
        return None

    doc_contour = sorted(doc_contours, key=cv2.contourArea, reverse=True)[0]
    return doc_contour


# ─────────────────────────────────────────────
# STEP 2 — Transparent overlay
# ─────────────────────────────────────────────
def draw_transparent_overlay(img, pts, color=(0, 200, 80)):
    """Draws a semi-transparent filled polygon over the document area."""
    
    overlay = img.copy()

    # Fill polygon
    cv2.fillPoly(overlay, [pts], color)

    # Blend
    alpha = 0.7
    result = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    return result


# ─────────────────────────────────────────────
# STEP 3 — Numbered corners
# ─────────────────────────────────────────────
def draw_numbered_corners(img, pts):
    """Draws numbered circles at each corner."""
    
    corner_colors = [(255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80)]
    
    for idx, (p, color) in enumerate(zip(pts, corner_colors), start=1):
        x, y = p[0][0], p[0][1]

        # Circle
        cv2.circle(img, (x, y), 20, color, -1)

        # Number text
        cv2.putText(
            img,
            str(idx),
            (x - 10, y + 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

    return img


# ─────────────────────────────────────────────
# STEP 4 — Status bar
# ─────────────────────────────────────────────
def draw_status_bar(img, text="Document detected — tap to scan"):
    """Adds a dark status bar at the bottom with white text."""
    
    result = img.copy()
    overlay = result.copy()

    h, w = result.shape[:2]
    bar_height = int(h * 0.12)

    # Rectangle
    cv2.rectangle(overlay, (0, h - bar_height), (w, h), (0, 0, 0), -1)

    # Blend
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, result, 1 - alpha, 0, result)

    # Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2

    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)

    text_x = (w - text_w) // 2
    text_y = h - (bar_height - text_h) // 2

    cv2.putText(
        result,
        text,
        (text_x, text_y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA
    )

    return result


# ─────────────────────────────────────────────
# STEP 5 — Full pipeline
# ─────────────────────────────────────────────
def scanner_preview(img):
    """Full scanner UI overlay."""
    
    result = img.copy()

    corners = find_document_corners(result)
    if corners is None:
        return result

    result = draw_transparent_overlay(result, corners)
    result = draw_numbered_corners(result, corners)
    result = draw_status_bar(result)

    return result


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
preview = scanner_preview(img)

if preview is not None:
    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('Scanner Preview UI')
    plt.tight_layout()
    plt.show()

    cv2.imwrite('../outputs/day36_preview.png', preview)
    print("Saved → outputs/day36_preview.png")


# ─────────────────────────────────────────────
# REFLECTION
# ─────────────────────────────────────────────
# Q1: What does the alpha parameter in addWeighted control?
# A1: It controls transparency (opacity) of the overlay.

# Q2: How would you add a "confidence score" percentage to the UI?
# A2: Use cv2.putText() to display a computed score (e.g., contour quality).
    