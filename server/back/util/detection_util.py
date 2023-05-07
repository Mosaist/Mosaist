def get_intersection_over_union(p, q):
    x1_1, y1_1, x2_1, y2_1 = (p['xmin'], p['ymin'], p['xmax'], p['ymax'])
    x1_2, y1_2, x2_2, y2_2 = (q['xmin'], q['ymin'], q['xmax'], q['ymax'])
    
    # 겹치는 영역 좌상단, 우하단 좌표 계산
    x_left = max(x1_1, x1_2)
    y_top = max(y1_1, y1_2)
    x_right = min(x2_1, x2_2)
    y_bottom = min(y2_1, y2_2)

    # 겹치는 영역의 너비와 높이 계산
    intersection_area = max(0, x_right - x_left + 1) * max(0, y_bottom - y_top + 1)

    # 전체 영역의 너비와 높이 계산
    box1_area = (x2_1 - x1_1 + 1) * (y2_1 - y1_1 + 1)
    box2_area = (x2_2 - x1_2 + 1) * (y2_2 - y1_2 + 1)

    # 두 영역의 합집합 면적 계산
    union_area = box1_area + box2_area - intersection_area

    # IoU 계산
    iou = intersection_area / union_area

    return iou

def apply_detections_nms(detections, iou_criteria=0.5):
    nms_applied = []

    for detection in detections:
        nms_applied_local = []

        detection.sort(key=lambda det: det['conf'])
        for i, det in enumerate(detection):
            keep = True
            for higher_conf_det in detection[i + 1:]:
                if get_intersection_over_union(det, higher_conf_det) > iou_criteria:
                    keep = False
                    break

            if keep:
                nms_applied_local.append(det)

        nms_applied.append(nms_applied_local)

    return nms_applied

def apply_detections_soft_nms(detections):
    return detections