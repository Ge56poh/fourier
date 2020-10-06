from math import pi, sin, cos

import sys

from typing import Dict

from svg_processor import SvgPath, determine_points, draw_result


def fourier_series(points: list, number_of_harmonics: int) -> Dict[int, complex]:
    """
    Performs the analysis of a discrete fourier series
    Calculates the complex fourier series coefficients, most likely called c_n
    The indices of the coefficients are symmetric to 0
    @param points: List of Points to consider
    @param number_of_harmonics: Number of frequencies to calculate
    @return: Dict containing values of the frequencies
    """
    period = len(points)
    end = number_of_harmonics // 2

    c_ret = {}

    c_0 = 0.0 + 0.0j
    for j in range(period):
        c_0 += points[j] / period

    for i in range(-end, end + 1):
        if i == 0:
            c_ret[0] = c_0
        else:
            a_i = 0.0 + 0.0j
            for j in range(period):
                a_i += 2 * (points[j] / period) * cos(2 * pi / period * i * j)
            b_i = 0.0 + 0.0j
            for j in range(period):
                b_i += 2 * (points[j] / period) * sin(2 * pi / period * i * j)
            c_ret[i] = (a_i - 0.0 + 1.0j * b_i) / 2

    return c_ret


if len(sys.argv) != 4:
    print('Usage: fourier <input-file> <output-file> <number of harmonics>\n')
else:
    svg = SvgPath(sys.argv[1])
    points = determine_points(svg.path, 20000)
    coefficients = fourier_series(points, int(sys.argv[3]))
    with open(sys.argv[2], mode='w') as fd:
        print(draw_result(svg, coefficients), file=fd)
    print("done\n")
