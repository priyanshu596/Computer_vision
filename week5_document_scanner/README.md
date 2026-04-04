# 📄 Week 5 — Document Scanner

**Goal:** Take a photo of a document at an angle → output a flat, clean, top-down scan.

**Pipeline you'll build piece by piece:**
```
Photo → Edge Detection → Find rectangle → Perspective warp → Clean output
```

## Learning Path

| Day | File | What you learn |
|-----|------|----------------|
| 31 | `day31_line_detector.py` | Canny + HoughLinesP |
| 32 | `day32_corner_detector.py` | Contours + approxPolyDP |
| 33 | `day33_perspective_correction.py` | getPerspectiveTransform + warpPerspective |
| 34 | `day34_document_enhancement.py` | adaptiveThreshold + sharpening |
| 35 | `day35_deskewer.py` | HoughLines + rotation correction |
| 36 | `day36_scanner_ui_overlay.py` | addWeighted + UI annotation |
| Project | `project_document_scanner.py` | Full pipeline |

## Key Functions This Week
- `cv2.Canny` — edge detection
- `cv2.HoughLinesP` — detect straight line segments
- `cv2.findContours` + `cv2.approxPolyDP` — find polygon shapes
- `cv2.getPerspectiveTransform` + `cv2.warpPerspective` — flatten perspective
- `cv2.adaptiveThreshold` — clean up document text
- `cv2.addWeighted` — blend two images (for UI overlay)

## Where This Leads (Deep Learning)
The pipeline you build here manually is exactly what **CRAFT** (Character Region Awareness for Text Detection) does — but learned from data. When you reach DL, swapping your edge detector for a pretrained CRAFT model will feel natural.
