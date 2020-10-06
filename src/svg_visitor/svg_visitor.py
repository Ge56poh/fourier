from abc import abstractmethod, ABC


########################################################################################################################
# svg structural classes
########################################################################################################################

# --- Svg --------------------------------------------------------------------------------------------------------------
class Svg:
    def __init__(self, width, height, options=None):
        self.width = str(width)
        self.height = str(height)
        self.options = str(
            options) if options is not None else 'xmlns="http://www.w3.org/2000/svg" ' \
                                                 'xmlns:xlink="http://www.w3.org/1999/xlink" '
        self.elements = []

    def append(self, elem):
        self.elements.append(elem)

    def accept(self, visitor):
        visitor.visit_svg(self)


########################################################################################################################
# Shapes

# --- Shape - abstract -------------------------------------------------------------------------------------------------
class Shape(ABC):
    def __init__(self, id=None, presentation_attr=None):
        self.id = str(id) if id is not None else None
        self.presentation_attr = str(presentation_attr) if presentation_attr is not None else None
        self.animations = []

    def append_animation(self, animation):
        self.animations.append(animation)

    def accept(self, visitor):
        visitor.visit_shape(self)


# --- Rectangle --------------------------------------------------------------------------------------------------------
class Rectangle(Shape):
    def __init__(self, width, height, x=None, y=None, rx=None, ry=None, id=None, presentation_attr=None):
        super().__init__(id=id, presentation_attr=presentation_attr)
        self.width = str(width)
        self.height = str(height)
        self.x = str(x) if x is not None else None
        self.y = str(y) if y is not None else None
        self.rx = str(rx) if rx is not None else None
        self.ry = str(ry) if ry is not None else None

    def accept(self, visitor):
        visitor.visit_rectangle(self)


# --- Circle -----------------------------------------------------------------------------------------------------------
class Circle(Shape):
    def __init__(self, r, cx=None, cy=None, id=None, presentation_attr=None):
        super().__init__(id=id, presentation_attr=presentation_attr)
        self.r = str(r)
        self.cx = str(cx) if cx is not None else None
        self.cy = str(cy) if cy is not None else None

    def accept(self, visitor):
        visitor.visit_circle(self)


# --- Ellipse ----------------------------------------------------------------------------------------------------------
class Ellipse(Shape):
    def __init__(self, rx, ry, cx=None, cy=None, id=None, presentation_attr=None):
        super().__init__(id=id, presentation_attr=presentation_attr)
        self.rx = str(rx)
        self.ry = str(ry)
        self.cx = str(cx) if cx is not None else None
        self.cy = str(cy) if cy is not None else None

    def accept(self, visitor):
        visitor.visit_ellipse(self)


# --- Line -------------------------------------------------------------------------------------------------------------
class Line(Shape):
    def __init__(self, x1, y1, x2, y2, id=None, presentation_attr=None):
        super().__init__(id=id, presentation_attr=presentation_attr)
        self.x1 = str(x1)
        self.y1 = str(y1)
        self.x2 = str(x2)
        self.y2 = str(y2)

    def accept(self, visitor):
        visitor.visit_line(self)


# --- Polygon ----------------------------------------------------------------------------------------------------------
class Polygon(Shape):
    def __init__(self, id=None, presentation_attr=None):
        super().__init__(id=id, presentation_attr=presentation_attr)
        self.points = []

    def add_point(self, x, y):
        self.points.append((x, y))

    def format_points(self):
        return ' points="' + ' '.join(str(x) + ',' + str(y) for (x, y) in self.points) + '"'

    def accept(self, visitor):
        visitor.visit_polygon(self)


# --- Polyline ---------------------------------------------------------------------------------------------------------
class Polyline(Shape):
    def __init__(self, id=None, presentation_attr=None):
        super().__init__(id=id, presentation_attr=presentation_attr)
        self.points = []

    def add_point(self, x, y):
        self.points.append((x, y))

    def format_points(self):
        return ' points="' + " ".join(str(x) + ',' + str(y) for x, y in self.points) + '"'

    def accept(self, visitor):
        visitor.visit_polyline(self)


# --- Path -------------------------------------------------------------------------------------------------------------
class Path(Shape):
    def __init__(self, id=None, presentation_attr=None):
        super().__init__(id=id, presentation_attr=presentation_attr)
        self.d = None

    def M(self, x, y):
        self.__append(" ".join(['M', str(x), str(y)]))

    def m(self, dx, dy):
        self.__append(" ".join(['m', str(dx), str(dy)]))

    def L(self, x, y):
        self.__append(" ".join(['L', str(x), str(y)]))

    def l(self, dx, dy):
        self.__append(" ".join(['l', str(dx), str(dy)]))

    def H(self, x):
        self.__append(" ".join(['H', str(x)]))

    def h(self, dx):
        self.__append(" ".join(['h', str(dx)]))

    def V(self, y):
        self.__append(" ".join(['V', str(y)]))

    def v(self, dy):
        self.__append(" ".join(['v', str(dy)]))

    def Z(self):
        self.__append(" ".join(['Z']))

    def C(self, cx1, cy1, cx2, cy2, ex, ey):
        self.__append(" ".join(['C', str(cx1), str(cy1), str(cx2), str(cy2), str(ex), str(ey)]))

    def c(self, cx1, cy1, cx2, cy2, ex, ey):
        self.__append(" ".join(['c', str(cx1), str(cy1), str(cx2), str(cy2), str(ex), str(ey)]))

    def S(self, cx2, cy2, ex, ey):
        self.__append(" ".join(['S', str(cx2), str(cy2), str(ex), str(ey)]))

    def s(self, cx2, cy2, ex, ey):
        self.__append(" ".join(['s', str(cx2), str(cy2), str(ex), str(ey)]))

    def Q(self, cx, cy, ex, ey):
        self.__append(" ".join(['Q', str(cx), str(cy), str(ex), str(ey)]))

    def q(self, cx, cy, ex, ey):
        self.__append(" ".join(['q', str(cx), str(cy), str(ex), str(ey)]))

    def T(self, ex, ey):
        self.__append(" ".join(['T', str(ex), str(ey)]))

    def t(self, ex, ey):
        self.__append(" ".join(['t', str(ex), str(ey)]))

    def A(self, rx, ry, rot, largeArc, sweep, ex, ey):
        self.__append(" ".join(['A', str(rx), str(ry), str(rot), str(int(bool(largeArc))),
                                str(int(bool(sweep))), str(ex), str(ey)]))

    def a(self, rx, ry, rot, largeArc, sweep, ex, ey):
        self.__append(" ".join(['a', str(rx), str(ry), str(rot), str(int(bool(largeArc))),
                                str(int(bool(sweep))), str(ex), str(ey)]))

    def set_path(self, path_string):
        self.d = path_string

    def __append(self, path_elem):
        if self.d is None:
            self.d = path_elem
        else:
            self.d += ' ' + path_elem

    def accept(self, visitor):
        visitor.visit_path(self)


# --- Text -------------------------------------------------------------------------------------------------------------
class Text(Shape):
    def __init__(self, text, xs: list = None, ys: list = None, dxs: list = None, dys: list = None, textLength=None,
                 rotates: list = None, id=None, presentation_attr=None):
        super().__init__(id=id, presentation_attr=presentation_attr)
        self.text = text
        self.textLength = str(textLength) if textLength is not None else None
        self.xs = ", ".join(str(x) for x in xs) if xs is not None else None
        self.ys = ", ".join(str(y) for y in ys) if ys is not None else None
        self.dxs = ", ".join(str(dx) for dx in dxs) if dxs is not None else None
        self.dys = ", ".join(str(dy) for dy in dys) if dys is not None else None
        self.rotates = ", ".join(str(rotate) for rotate in rotates) if rotates is not None else None

    def accept(self, visitor):
        visitor.visit_text(self)


########################################################################################################################
# Animations

# --- Animation - abstract ---------------------------------------------------------------------------------------------
class Animation(ABC):
    def __init__(self, dur=None, repeatCount=None, animation_attr=None):
        self.dur = str(dur) if dur is not None else None
        self.repeatCount = str(repeatCount) if repeatCount is not None else None
        self.animation_attr = str(animation_attr) if animation_attr is not None else None

    def accept(self, visitor):
        visitor.visit_animation(self)


# --- Animate ----------------------------------------------------------------------------------------------------------
class Animate(Animation):
    def __init__(self, attribute_name, by=None, from_=None, to=None, dur=None, repeatCount=None, animation_attr=None):
        super().__init__(dur, repeatCount, animation_attr)
        self.attribute_name = str(attribute_name)
        self.by = str(by) if by is not None else None
        self.from_ = str(from_) if from_ is not None else None
        self.to = str(to) if to is not None else None

    def accept(self, visitor):
        visitor.visit_animate(self)


# --- AnimateMotion ----------------------------------------------------------------------------------------------------
class AnimateMotion(Animation):
    def __init__(self, path: Path, keyPoints: list = None, keyTimes: list = None, calcMode=None, dur=None,
                 repeatCount=None,
                 animation_attr=None):
        super().__init__(dur, repeatCount, animation_attr)
        self.path = path
        self.calcMode = str(calcMode) if calcMode is not None else None
        self.keyPoints = ";".join(list(map(lambda s: str(s), keyPoints))) if keyPoints is not None else None
        self.keyTimes = ";".join(list(map(lambda s: str(s), keyTimes))) if keyTimes is not None else None

    def accept(self, visitor):
        visitor.visit_animate_motion(self)


# --- AnimateTransform -------------------------------------------------------------------------------------------------
class AnimateTransform(Animation):
    def __init__(self, type, by=None, from_=None, to=None, dur=None, repeatCount=None, animation_attr=None):
        super().__init__(dur, repeatCount, animation_attr)
        self.type = str(type) if type is not None else None
        self.by = str(by) if by is not None else None
        self.from_ = str(from_) if from_ is not None else None
        self.to = str(to) if to is not None else None

    def accept(self, visitor):
        visitor.visit_animate_transform(self)


########################################################################################################################
# Group

class Group:
    def __init__(self, id=None, presentation_attr=None):
        self.id = str(id) if id is not None else None
        self.presentation_attr = str(presentation_attr) if presentation_attr is not None else None
        self.elements = []
        self.animations = []

    def append_element(self, element):
        self.elements.append(element)

    def append_animation(self, animation):
        self.animations.append(animation)

    def accept(self, visitor):
        visitor.visit_group(self)


########################################################################################################################
# visitors
########################################################################################################################

class Visitor(ABC):
    @abstractmethod
    def visit_svg(self, svg: Svg):
        pass

    @abstractmethod
    def visit_shape(self, shape: Shape):
        pass

    @abstractmethod
    def visit_rectangle(self, rect: Rectangle):
        pass

    @abstractmethod
    def visit_circle(self, circ: Circle):
        pass

    @abstractmethod
    def visit_ellipse(self, ellip: Ellipse):
        pass

    @abstractmethod
    def visit_line(self, line: Line):
        pass

    @abstractmethod
    def visit_polygon(self, polygon: Polygon):
        pass

    @abstractmethod
    def visit_polyline(self, polyline: Polyline):
        pass

    @abstractmethod
    def visit_path(self, path: Path):
        pass

    @abstractmethod
    def visit_text(self, text: Text):
        pass

    @abstractmethod
    def visit_animation(self, animation: Animation):
        pass

    @abstractmethod
    def visit_animate(self, animate: Animate):
        pass

    @abstractmethod
    def visit_animate_motion(self, motion: AnimateMotion):
        pass

    @abstractmethod
    def visit_animate_transform(self, transform: AnimateTransform):
        pass

    @abstractmethod
    def visit_group(self, group: Group):
        pass


# noinspection PyShadowingNames
class FormatVisitor(Visitor):
    def __init__(self):
        self.header_str = []
        self.elements_str = []
        self.defs_str = []
        self.footer_str = []

        self.indent = 0

        self.id_counter = 0
        self.elements = []
        self.defs = []

    def visit_svg(self, svg: Svg):
        self.__indent(self.header_str)
        self.header_str += '<svg'

        self.header_str += ' width="'
        self.header_str += svg.width
        self.header_str += '"'

        self.header_str += ' height="'
        self.header_str += svg.height
        self.header_str += '"'

        if svg.options is not None:
            self.header_str += ' ' + svg.options

        self.header_str += '>'
        self.header_str += '\n'

        self.indent += 1
        for elem in svg.elements:
            elem.accept(self)
        self.indent -= 1

        if len(set(self.defs).difference(self.elements)) != 0:
            tmp = self.elements_str
            self.elements_str = []

            self.__indent(self.elements_str)
            self.elements_str += '<defs>'
            self.indent += 1
            for def_ in self.defs:
                if def_ not in self.elements:
                    def_.accept(self)
            self.indent -= 1
            self.__indent(self.elements_str)
            self.elements_str += '</defs>\n'

            self.defs_str = self.elements_str
            self.elements_str = tmp

        self.__indent(self.footer_str)
        self.footer_str += '</svg>'

    def visit_shape(self, shape: Shape):
        if shape.id is None:
            shape.id = 'e' + str(self.id_counter)
            self.id_counter += 1
        self.elements_str += ' id="'
        self.elements_str += shape.id
        self.elements_str += '"'
        self.elements.append(shape)

        if shape.presentation_attr is not None:
            self.elements_str += ' ' + shape.presentation_attr

        self.elements_str += '>'
        self.elements_str += '\n'

        self.indent += 1
        for animation in shape.animations:
            animation.accept(self)
        self.indent -= 1

    def visit_rectangle(self, rect: Rectangle):
        self.__indent(self.elements_str)
        self.elements_str += '<rect'

        self.elements_str += ' width="'
        self.elements_str += rect.width
        self.elements_str += '"'

        self.elements_str += ' height="'
        self.elements_str += rect.height
        self.elements_str += '"'

        if rect.x is not None:
            self.elements_str += ' x="'
            self.elements_str += rect.x
            self.elements_str += '"'

        if rect.y is not None:
            self.elements_str += ' y="'
            self.elements_str += rect.y
            self.elements_str += '"'

        if rect.rx is not None:
            self.elements_str += ' rx="'
            self.elements_str += rect.rx
            self.elements_str += '"'

        if rect.ry is not None:
            self.elements_str += ' ry="'
            self.elements_str += rect.ry
            self.elements_str += '"'

        super(Rectangle, rect).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</rect>'
        self.elements_str += '\n'

    def visit_circle(self, circle: Circle):
        self.__indent(self.elements_str)
        self.elements_str += '<circle'

        self.elements_str += ' r="'
        self.elements_str += circle.r
        self.elements_str += '"'

        if circle.cx is not None:
            self.elements_str += ' cx="'
            self.elements_str += circle.cx
            self.elements_str += '"'

        if circle.cy is not None:
            self.elements_str += ' cy="'
            self.elements_str += circle.cy
            self.elements_str += '"'

        super(Circle, circle).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</circle>'
        self.elements_str += '\n'

    def visit_ellipse(self, ellip: Ellipse):
        self.__indent(self.elements_str)
        self.elements_str += '<ellipse'

        self.elements_str += ' rx="'
        self.elements_str += ellip.rx
        self.elements_str += '"'

        self.elements_str += ' ry="'
        self.elements_str += ellip.ry
        self.elements_str += '"'

        if ellip.cx is not None:
            self.elements_str += ' cx="'
            self.elements_str += ellip.cx
            self.elements_str += '"'

        if ellip.cy is not None:
            self.elements_str += ' cy="'
            self.elements_str += ellip.cy
            self.elements_str += '"'

        super(Ellipse, ellip).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</ellipse>'
        self.elements_str += '\n'

    def visit_line(self, line: Line):
        self.__indent(self.elements_str)
        self.elements_str += '<line'

        self.elements_str += ' x1="'
        self.elements_str += line.x1
        self.elements_str += '"'

        self.elements_str += ' y1="'
        self.elements_str += line.y1
        self.elements_str += '"'

        self.elements_str += ' x2="'
        self.elements_str += line.x2
        self.elements_str += '"'

        self.elements_str += ' y2="'
        self.elements_str += line.y2
        self.elements_str += '"'

        super(Line, line).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</line>'
        self.elements_str += '\n'

    def visit_polygon(self, polygon: Polygon):
        self.__indent(self.elements_str)
        self.elements_str += '<polygon'

        self.elements_str += polygon.format_points()

        super(Polygon, polygon).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</polygon>'
        self.elements_str += '\n'

    def visit_polyline(self, polyline: Polyline):
        self.__indent(self.elements_str)
        self.elements_str += '<polyline'

        self.elements_str += polyline.format_points()

        super(Polyline, polyline).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</polyline>'
        self.elements_str += '\n'

    def visit_path(self, path: Path):
        self.__indent(self.elements_str)
        self.elements_str += '<path'

        if path.d is not None:
            self.elements_str += ' d="' + path.d + '"'

        super(Path, path).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</path>'
        self.elements_str += '\n'

    def visit_text(self, text: Text):
        self.__indent(self.elements_str)
        self.elements_str += '<text'

        if text.textLength is not None:
            self.elements_str += ' textLength="'
            self.elements_str += text.textLength
            self.elements_str += '"'

        if text.xs is not None:
            self.elements_str += ' x="'
            self.elements_str += text.xs
            self.elements_str += '"'

        if text.ys is not None:
            self.elements_str += ' y="'
            self.elements_str += text.ys
            self.elements_str += '"'

        if text.dxs is not None:
            self.elements_str += ' dx="'
            self.elements_str += text.dxs
            self.elements_str += '"'

        if text.dys is not None:
            self.elements_str += ' dy="'
            self.elements_str += text.dys
            self.elements_str += '"'

        if text.rotates is not None:
            self.elements_str += ' rotate="'
            self.elements_str += text.rotates
            self.elements_str += '"'

        super(Text, text).accept(self)

        self.indent += 1
        self.__indent(self.elements_str)
        self.indent -= 1
        self.elements_str += text.text
        self.elements_str += '\n'

        self.__indent(self.elements_str)
        self.elements_str += '</text>'
        self.elements_str += '\n'

    def visit_animation(self, animation: Animation):
        if animation.dur is not None:
            self.elements_str += ' dur="'
            self.elements_str += animation.dur
            self.elements_str += '"'

        if animation.repeatCount is not None:
            self.elements_str += ' repeatCount="'
            self.elements_str += animation.repeatCount
            self.elements_str += '"'

        if animation.animation_attr is not None:
            self.elements_str += ' ' + animation.animation_attr

        self.elements_str += '>'
        self.elements_str += '\n'

    def visit_animate(self, animate: Animate):
        self.__indent(self.elements_str)
        self.elements_str += '<animate'

        self.elements_str += ' attributeName="'
        self.elements_str += animate.attribute_name
        self.elements_str += '"'

        if animate.by is not None:
            self.elements_str += ' by="'
            self.elements_str += animate.by
            self.elements_str += '"'

        if animate.from_ is not None:
            self.elements_str += ' from="'
            self.elements_str += animate.from_
            self.elements_str += '"'

        if animate.to is not None:
            self.elements_str += ' to="'
            self.elements_str += animate.to
            self.elements_str += '"'

        super(Animate, animate).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</animate>'
        self.elements_str += '\n'

    def visit_animate_motion(self, motion: AnimateMotion):
        self.__indent(self.elements_str)
        self.elements_str += '<animateMotion'

        # if motion.path.d is not None:
        #    self.elements_str += ' path="'
        #    self.elements_str += motion.path.d
        #    self.elements_str += '"'

        if motion.keyPoints is not None:
            self.elements_str += ' keyPoints="'
            self.elements_str += motion.keyPoints
            self.elements_str += '"'

        if motion.keyTimes is not None:
            self.elements_str += ' keyTimes="'
            self.elements_str += motion.keyTimes
            self.elements_str += '"'

        if motion.calcMode is not None:
            self.elements_str += ' calcMode="'
            self.elements_str += motion.calcMode
            self.elements_str += '"'

        super(AnimateMotion, motion).accept(self)

        self.indent += 1
        self.__indent(self.elements_str)
        self.elements_str += '<mpath xlink:href="#'
        if motion.path.id is None:
            motion.path.id = 'e' + str(self.id_counter)
            self.id_counter += 1
        self.elements_str += motion.path.id
        self.elements_str += '"/>\n'
        self.indent -= 1
        self.defs.append(motion.path)

        self.__indent(self.elements_str)
        self.elements_str += '</animateMotion>'
        self.elements_str += '\n'

    def visit_animate_transform(self, transform: AnimateTransform):
        self.__indent(self.elements_str)
        self.elements_str += '<animateTransform attributeName="transform"'

        self.elements_str += ' type="'
        self.elements_str += transform.type
        self.elements_str += '"'

        if transform.by is not None:
            self.elements_str += ' by="'
            self.elements_str += transform.by
            self.elements_str += '"'

        if transform.from_ is not None:
            self.elements_str += ' from="'
            self.elements_str += transform.from_
            self.elements_str += '"'

        if transform.to is not None:
            self.elements_str += ' to="'
            self.elements_str += transform.to
            self.elements_str += '"'

        super(AnimateTransform, transform).accept(self)

        self.__indent(self.elements_str)
        self.elements_str += '</animateTransform>'
        self.elements_str += '\n'

    def visit_group(self, group: Group):
        self.__indent(self.elements_str)
        self.elements_str += '<g'

        if group.id is not None:
            self.elements_str += ' id="'
            self.elements_str += group.id
            self.elements_str += '"'

        if group.presentation_attr is not None:
            self.elements_str += ' '
            self.elements_str += group.presentation_attr

        self.elements_str += '>\n'
        #self.indent += 1

        for elem in group.elements:
            elem.accept(self)

        for anim in group.animations:
            anim.accept(self)

        #self.indent -= 1
        self.__indent(self.elements_str)
        self.elements_str += '</g>\n'

    def __indent(self, list):
        tmp = ''
        for _ in range(self.indent):
            tmp += '\t'
        list += tmp

    def formatted(self):
        return "".join(
            ["".join(self.header_str), "".join(self.defs_str), "".join(self.elements_str), "".join(self.footer_str)])


########################################################################################################################
# test
########################################################################################################################

#svg = Svg(480.0, 480.0)

# rect = Rectangle(20, 20, 5, 5, presentation_attr='fill="blue"')
# svg.append(rect)

# circle = Circle(20, 5, 5, presentation_attr='fill="green"')
# svg.append(circle)

# ellipse = Ellipse(5, 5, 10, 10, presentation_attr='stroke="black" fill="red"')
# svg.append(ellipse)

# line = Line(3, 3, 5, 7, presentation_attr='stroke="black"')
# svg.append(line)

# polygon = Polygon(presentation_attr='stroke="black" fill="red"')
# polygon.add_point(5, 5)
# polygon.add_point(15, 15)
# polygon.add_point(5, 50)
# svg.append(polygon)

# polyline = Polyline(presentation_attr='stroke="black"')
# polyline.add_point(50, 50)
# polyline.add_point(75, 15)
# polyline.add_point(5, 50)
# svg.append(polyline)

# text = Text("Test", [25, 30], [25, 30])
# svg.append(text)

#path = Path(presentation_attr='stroke="black" fill="none"')
#path.m(200.091, 20.094)
#path.c(-9.325, 0.0, -18.67, 1.19, -27.614, 2.557)
#path.c(-1.422, 22.928, -5.023, 45.308, -24.034, 53.182)
#path.c(-19.054, 7.892, -36.952, -5.717, -54.204, -20.966)
#path.c(-15.084, 11.01, -28.864, 24.3, -39.886, 39.376)
#path.c(15.309, 17.301, 29.396, 35.09, 21.478, 54.204)
#path.c(-7.909, 19.094, -30.662, 22.622, -53.694, 24.034)
#path.c(-1.4, 9.046, -2.045, 18.176, -2.045, 27.614)
#path.c(0.0, 9.559, 0.612, 18.969, 2.045, 28.124)
#path.c(23.032, 1.41, 45.784, 3.918, 53.694, 23.012)
#path.c(7.918, 19.115, -6.168, 37.926, -21.478, 55.228)
#path.c(10.967, 14.962, 24.91, 27.914, 39.886, 38.864)
#path.c(17.197, -15.182, 35.218, -28.32, 54.204, -20.454)
#path.c(19.094, 7.909, 22.622, 30.15, 24.034, 53.182)
#path.c(8.943, 1.368, 18.288, 2.045, 27.614, 2.045)
#path.c(9.326, 0.0, 18.159, -0.68, 27.102, -2.045)
#path.c(1.41, -23.032, 4.941, -45.274, 24.034, -53.182)
#path.c(18.987, -7.865, 37.008, 5.272, 54.204, 20.454)
#path.c(14.975, -10.95, 28.918, -23.902, 39.886, -38.864)
#path.c(-15.309, -17.301, -29.396, -36.112, -21.478, -55.228)
#path.c(7.909, -19.094, 31.172, -21.6, 54.204, -23.012)
#path.c(1.434, -9.156, 2.045, -18.566, 2.045, -28.124)
#path.c(0.0, -9.438, -0.648, -18.567, -2.045, -27.614)
#path.c(-23.032, -1.41, -46.296, -4.941, -54.204, -24.034)
#path.c(-7.918, -19.115, 6.168, -36.904, 21.478, -54.204)
#path.c(-11.022, -15.075, -24.802, -28.366, -39.886, -39.376)
#path.c(-17.252, 15.249, -35.152, 28.858, -54.204, 20.966)
#path.c(-19.011, -7.875, -22.612, -30.254, -24.034, -53.182)
#path.c(-8.943, -1.368, -17.777, -2.557, -27.102, -2.557)
#path.Z()
#path.m(0.0, 121.194)
#path.c(32.522, 0.0, 58.806, 26.284, 58.806, 58.806)
#path.s(-26.284, 58.806, -58.806, 58.806)
#path.s(-59.318, -26.284, -59.318, -58.806)
#path.s(26.796, -58.806, 59.318, -58.806)
#path.Z()

# animate_tranform = AnimateTransform('rotate', from_='0', to='360', dur='10s', repeatCount='indefinite')
# path.append_animation(animate_tranform)

#animate_path = Path()
#animate_motion = AnimateMotion(animate_path, keyPoints=[0, 1], keyTimes=[0, 1], calcMode="linear", dur='1s',
#                               repeatCount='indefinite')
#animate_path.m(25, 25)
#animate_path.l(50, 0)
#animate_path.l(0, 50)
#animate_path.l(-50, 0)
#animate_path.l(0, -50)
#path.append_animation(animate_motion)

#svg.append(path)

#vis = FormatVisitor()
#svg.accept(vis)
#print(vis.formatted())
