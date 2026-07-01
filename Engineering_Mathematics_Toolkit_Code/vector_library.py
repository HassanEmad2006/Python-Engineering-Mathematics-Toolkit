import math


def _to_numbers(vector):
    return [float(component) for component in vector]


def _pad_vectors(vector1, vector2):
    size = max(len(vector1), len(vector2))
    if size not in (2, 3):
        raise ValueError('Vectors must have 2 or 3 components.')
    padded1 = vector1 + [0.0] * (size - len(vector1))
    padded2 = vector2 + [0.0] * (size - len(vector2))
    return padded1, padded2


def _format_number(value):
    if abs(value - round(value)) < 1e-10:
        return str(int(round(value)))
    return f'{value:.10g}'


def vector_coordinates(vector):
    vector = _to_numbers(vector)
    if len(vector) not in (2, 3):
        raise ValueError('Vectors must have 2 or 3 components.')

    labels = ['i', 'j', 'k']
    parts = []
    for index, value in enumerate(vector):
        if abs(value) < 1e-12:
            continue
        label = labels[index]
        number = _format_number(abs(value))
        if not parts:
            parts.append(f'{"-" if value < 0 else ""}{number}{label}')
        else:
            sign = '-' if value < 0 else '+'
            parts.append(f' {sign} {number}{label}')
    return ''.join(parts) if parts else '0'


def magnitude(vector):
    vector = _to_numbers(vector)
    if len(vector) not in (2, 3):
        raise ValueError('Vectors must have 2 or 3 components.')
    return math.sqrt(sum(component ** 2 for component in vector))


def angle_with_axis(vector):
    vector = _to_numbers(vector)
    if len(vector) == 2:
        return math.atan2(vector[1], vector[0])
    if len(vector) == 3:
        vector_magnitude = magnitude(vector)
        if vector_magnitude == 0:
            raise ValueError('Angle is undefined for the zero vector.')
        return (
            math.acos(max(-1.0, min(1.0, vector[0] / vector_magnitude))),
            math.acos(max(-1.0, min(1.0, vector[1] / vector_magnitude))),
            math.acos(max(-1.0, min(1.0, vector[2] / vector_magnitude))),
        )
    raise ValueError('Vectors must have 2 or 3 components.')


def dot(vector1, vector2):
    vector1 = _to_numbers(vector1)
    vector2 = _to_numbers(vector2)
    vector1, vector2 = _pad_vectors(vector1, vector2)
    return sum(component1 * component2 for component1, component2 in zip(vector1, vector2))


def angle_between_vectors(vector1, vector2):
    vector1 = _to_numbers(vector1)
    vector2 = _to_numbers(vector2)
    vector1, vector2 = _pad_vectors(vector1, vector2)
    denominator = magnitude(vector1) * magnitude(vector2)
    if denominator == 0:
        raise ValueError('Angle is undefined for the zero vector.')
    cosine_value = max(-1.0, min(1.0, dot(vector1, vector2) / denominator))
    return math.acos(cosine_value)


def cross_product(vector1, vector2):
    vector1 = _to_numbers(vector1)
    vector2 = _to_numbers(vector2)
    vector1, vector2 = _pad_vectors(vector1, vector2)
    if len(vector1) == 2:
        return vector1[0] * vector2[1] - vector1[1] * vector2[0]

    return [
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0],
    ]


def magnitute_of_cross(vector1, vector2):
    result = cross_product(vector1, vector2)
    if isinstance(result, list):
        return math.sqrt(sum(component ** 2 for component in result))
    return abs(result)


def rad_to_degree(angle):
    return angle * (180 / math.pi)


def degree_angle_in_3d(vector):
    vector = _to_numbers(vector)
    if len(vector) != 3:
        raise ValueError('Vector must have 3 components.')
    vector_magnitude = magnitude(vector)
    if vector_magnitude == 0:
        raise ValueError('Angle is undefined for the zero vector.')
    return (
        rad_to_degree(math.acos(max(-1.0, min(1.0, vector[0] / vector_magnitude)))),
        rad_to_degree(math.acos(max(-1.0, min(1.0, vector[1] / vector_magnitude)))),
        rad_to_degree(math.acos(max(-1.0, min(1.0, vector[2] / vector_magnitude)))),
    )