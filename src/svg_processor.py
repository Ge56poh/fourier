import cmath
import re

import numpy as np
from svg.path import parse_path
from typing import List, Dict

from svg_visitor.svg_visitor import *

duration = 20


class SvgPath:
    """
    Represents a Svg-Path
    """

    def __init__(self, file_path: str):
        with open(file_path, 'r') as fd:
            content = fd.read()

        re_height = "<svg[^>]*height=\"([0-9.]*)\".*"
        re_width = "<svg[^>]*width=\"([0-9.]*)\".*"
        match_height = re.search(re_height, content)
        match_width = re.search(re_width, content)

        if match_height is None or match_width is None:
            re_viewBox = "<svg[^>]*viewBox=\"([0-9. ]*)\".*"
            match_viewBox = re.search(re_viewBox, content)
            numbers = match_viewBox.group(1)
            re_dims = "[0-9.]* [0-9.]* ([0-9.]*) ([0-9.]*)"
            match_dims = re.search(re_dims, numbers)
            width = match_dims.group(1)
            height = match_dims.group(2)
        else:
            height = match_height.group(1)
            width = match_width.group(1)

        re_path = "<path.*d=\"([MLHVCSQTAZmlhvcsqtaz0-9- ,;.]*)\".*/>"
        self.height = float(height)
        self.width = float(width)
        self.path = re.findall(re_path, content)[0]


def determine_points(path_desc: str, number_of_points: int) -> List[complex]:
    """
    Extracts equidistant points from a given description of a svg-Path
    :param path_desc: path description in string format
    :param number_of_points:
    :return:
    """
    # parse path
    path = parse_path(path_desc)

    # calculate points
    ret = []
    for i in range(number_of_points):
        ret.append(path.point(i * (1 / number_of_points)))
    return ret


def draw_result(svg: SvgPath, harmonics: Dict[int, complex]):
    """
    Draws circles and arrows representing the fourier series on top of the svg-Path
    :param svg: SvgPath object to draw on
    :param harmonics: calculated fourier coefficients
    :return: string in svg-format
    """
    d = Svg(svg.width * 1.2, svg.height * 1.2)

    ####################################################################################################################
    # draw original path
    ####################################################################################################################

    path = Path(
        presentation_attr='stroke="black" fill="none"')
    path.set_path(svg.path)
    d.append(path)

    ####################################################################################################################
    # draw circles and arrows
    ####################################################################################################################

    number_harmonics = len(harmonics)
    end = number_harmonics // 2

    circles = {}
    groups_freq = {}
    groups_anim = {}

    for i in range(1, end + 1):
        # positive frequency
        amplitude = abs(harmonics[i])
        circle_pos = __circle_to_path(0, 0, amplitude,
                                      presentation_attr='stroke="blue" fill="none" stroke-width="0.5" stroke-dasharray="1,1"')
        arrow_pos = Line(0, 0, amplitude, 0, presentation_attr='stroke="blue" fill="none" stroke-width="0.5"')
        circles[i] = circle_pos

        # negative frequency
        amplitude = abs(harmonics[-i])
        circle_neg = __circle_to_path(0, 0, amplitude, direction=1,
                                      presentation_attr='stroke="blue" fill="none" stroke-width="0.5" stroke-dasharray="1,1"')
        arrow_neg = Line(0, 0, amplitude, 0, presentation_attr='stroke="blue" fill="none" stroke-width="0.5"')
        circles[-i] = circle_neg

        # positive group
        group_pos = Group(id='c' + str(i))
        groups_freq[i] = group_pos

        group_pos.append_element(circle_pos)
        group_pos.append_element(arrow_pos)

        # negative group
        group_neg = Group(id='c' + str(-i))
        groups_freq[-i] = group_neg

        group_neg.append_element(circle_neg)
        group_neg.append_element(arrow_neg)

    for i in range(end, 0, -1):
        # positive to negative
        group = Group(id='a' + str(i))
        group.append_element(groups_freq[i])
        if i != end:
            group.append_element(groups_anim[-(i + 1)])
        else:
            c = Circle(svg.width / 200, 0, 0, presentation_attr='stroke="black" fill="red"')
            group.append_element(c)

        groups_anim[i] = group

        # negative to next positive
        if i != 1:
            group = Group(id='a' + str(-i))
        else:
            group = Group(id='a' + str(-i),
                          presentation_attr='transform="translate(' + str(harmonics[0].real) + ' ' + str(
                              harmonics[0].imag) + ')"')

        group.append_element(groups_freq[-i])
        group.append_element(groups_anim[i])
        groups_anim[-i] = group

    ####################################################################################################################
    # animate
    ####################################################################################################################

    for i in range(1, end + 1):
        # negative
        from_str = str(np.degrees(cmath.phase(harmonics[-i]))) + " 0 0"
        to_str = str(np.degrees(cmath.phase(harmonics[-i])) + 360) + " 0 0"
        animation = AnimateTransform('rotate', dur=str(1 / i * duration) + 's',
                                     from_=from_str, to=to_str, repeatCount='indefinite')
        groups_freq[-i].append_animation(animation)

        # positive
        from_str = str(np.degrees(cmath.phase(harmonics[i])) + 360) + " 0 0"
        to_str = str(np.degrees(cmath.phase(harmonics[i]))) + " 0 0"
        animation = AnimateTransform('rotate', dur=str(1 / i * duration) + 's',
                                     from_=from_str, to=to_str, repeatCount='indefinite')
        groups_freq[i].append_animation(animation)

    for i in range(1, end + 1):
        # attach negative one below to positive
        if i != 1:
            start = ((-cmath.phase(harmonics[i - 1]) / (2 * cmath.pi)) + 0.5) % 1.0
            key_points = [start, 1, 0, start]
            key_times = [0, 1 - start, 1 - start, 1]
            animation = AnimateMotion(circles[(i - 1)], dur=str(1 / abs(i - 1) * duration) + 's',
                                      repeatCount='indefinite', keyPoints=key_points, keyTimes=key_times,
                                      calcMode='linear')
            groups_anim[-i].append_animation(animation)

        # attach positive to negative
        start = ((cmath.phase(harmonics[-i]) / (2 * cmath.pi)) + 0.5) % 1.0
        key_points = [start, 1, 0, start]
        key_times = [0, 1 - start, 1 - start, 1]
        animation = AnimateMotion(circles[-i], dur=str(1 / abs(i) * duration) + 's',
                                  repeatCount='indefinite', keyPoints=key_points, keyTimes=key_times,
                                  calcMode='linear')
        groups_anim[i].append_animation(animation)

    start = ((-cmath.phase(harmonics[end]) / (2 * cmath.pi)) + 0.5) % 1.0
    key_points = [start, 1, 0, start]
    key_times = [0, 1 - start, 1 - start, 1]
    animation = AnimateMotion(circles[end], dur=str(1 / abs(end) * duration) + 's',
                              repeatCount='indefinite', keyPoints=key_points, keyTimes=key_times,
                              calcMode='linear')
    c.append_animation(animation)

    d.append(groups_anim[-1])

    visitor = FormatVisitor()
    d.accept(visitor)
    return visitor.formatted()


def __circle_to_path(x:float, y:float, r:float, direction=0, presentation_attr=None) -> Path:
    """
    Creates a circle in form of a path
    @param x: x coordinate of center
    @param y: y coordinate of center
    @param r: radius
    @param direction: direction in witch to draw
    @param presentation_attr: svg drawing attributes
    @return:
    """
    p = Path(presentation_attr=presentation_attr)
    p.M(x - r, y)
    p.a(r, r, 0, 1, direction, 2 * r, 0)
    p.a(r, r, 0, 1, direction, -2 * r, 0)
    return p
