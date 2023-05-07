def get_area(b):
    w = b['xmax'] - b['xmin']
    h = b['ymax'] - b['ymin']

    return w * h

def get_inter(p, q):
    if p['xmin'] > q['xmax']:
        return False
    elif p['xmax'] < q['xmin']:
        return False
    if p['ymin'] > q['ymax']:
        return False
    elif p['ymax'] < q['ymax']:
        return False

    return {
        'xmin': max(p['xmin'], q['xmin']),
        'xmax': min(p['xmax'], q['xmax']),
        'ymin': max(p['ymin'], q['ymin']),
        'ymax': min(p['ymax'], q['ymax'])
    }

def get_intersection_of_union(p, q):
    area_p = get_area(p)
    area_q = get_area(q)
    
    inter = get_inter(p, q)

    if not inter:
        return 0

    area_inter = get_area(inter)
    return area_inter / (area_p + area_q - area_inter)

def apply_detections_nms(detections):
    nms_applied = []

    for detection in detections:
        nms_applied_local = []

        detection.sort(key=lambda det: det['conf'])
        for i, det in enumerate(detection):
            keep = True
            for higher_conf_det in detection[i + 1:]:
                if get_intersection_of_union(det, higher_conf_det) > 0:
                    keep = False
                    break

            if keep:
                nms_applied_local.append(det)

        nms_applied.append(nms_applied_local)

    return nms_applied

def apply_detections_soft_nms(detections):
    return detections