
import pickle


class ImageError(Exception): pass
class CoordinateError(ImageError):pass
class NoFilenameError(ImageError): pass
class LoadError(ImageError): pass
class SaveError(ImageError): pass

class Image:

    def __init__(self, width, height, filename = "",
            background='#FFFFFF'):
        '''
        声明Image类
        __data为一个字典,键为(x,y)的坐标,值为其颜色
        __colors为画布上的颜色
        '''
        self.filename = filename
        self.__background = background
        self.__data = {}
        self.__width = width
        self.__height = height 
        self.__colors = {self.__background}

    # 使用特性对私有对象进行访问,而没有使用 __getattr__, 或者 __setattr__
    @property
    def background(self):
        return self.__background

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
    
    @property
    def colors(self):
        '''
        这样直接返回一个可变类型是不安全的.但是我未发现如何就现有格式进行威胁.
        最好这样:
        return set(self.__data.values())|{self.__background}
        '''
        return set(self.__colors)

    def detection_coordinate(self, coordinate):
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.__width) or not (0 <= coordinate[1] < self.__height)):
            raise CoordinateError(str(coordinate))


    def __getitem__(self, coordinate):
        '''
        返回所给坐标的颜色

        get中使用了tuple(coordinate),保证格式正确
        要是传入一个list,由于list未支持hash,所以会报错.
        '''
        self.detection_coordinate(coordinate)
        return self.__data.get(tuple(coordinate), self.__background)

    def __setitem__(self, coordinate, color):
        '''
        使用pop方法而不是del方法
        因为del方法会产生一个异常,这里就是避免异常
        毕竟,给一个边界外的点一个颜色没有意义,所以对于无意义的事情,不报异常也可以吧....
        '''
        self.detection_coordinate(coordinate)

        if color == self.__background:
            self.__data.pop(tuple(coordinate), None)
        else:
            self.__data[tuple(coordinate)] = color
            self.__colors.add(color)

    def __delitem__(self, coordinate):
        self.detection_coordinate(coordinate)
        self.__data.pop(tuple(coordinate), None)

    '''
    使用pickle进行序列化
    注意,pickle没有加密或者数字签名,导致其是不安全的
    '''
    def save(self, filename = None):
        '''
        pickle.HIGHEST_PROTOCOL(3.5为4, pickle.DEFAULT_PROTOCOL为3) 为紧凑的二进制
        所以需要wb
        这里data没有存储colors,而是在读取的时候重构colors~ 保证跟实际内容相符
        '''
        if filename is not None:
            self.filename = filename
        else:
            raise NoFileNameError()
        
        fh = None
        try:
            data = [self.width, self.height, self.__background,
                    self.__data]
            fh = open(self.filename, 'wb')
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PickleError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def load(self, filename = None):
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            fh = open(self.filename, "rb")
            data = pickle.load(fh)
            (self.__width, self.__height, self.__background,
             self.__data) = data
            self.__colors = (set(self.__data.values()) |
                             {self.__background})
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))
        finally:
            if fh is not None:
                fh.close()        
        
    def export(self, filename):
        """Exports the image to the specified filename
        """
        if filename.lower().endswith(".xpm"):
            self.__export_xpm(filename)
        else:
            raise ExportError("unsupported export format: " +
                              os.path.splitext(filename)[1])

    def __export_xpm(self, filename):
        pass


    def resize(self, width = None, height = None):
        '''
        想象一下可能的情况
        1.width和height均为空,那么原对象不变,返回False
        2.width和height均大于原对象的值,那么只要将width和height赋给__width和__height就可以了
          不涉及到__data和__colors的变化
        3.如果width和height中有一个小于原对象中的值,那么就要进行对比,然后删除了
        '''
        if width is None and height is None:
            return False
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if width >= self.width and height >= self.height:
            '''
            如果所给长宽大于默认,则其背景均为默认背景,不需改变
            '''
            self.__width = width
            self.__height = height
            return True

        self.__width = width 
        self.__height = height 
        for x, y in list(self.__data.keys()):
            if x >= self.width or y >= self.height:
                del self.__data[(x, y)]
        self.__colors = set(self.__data.values()) | {self.__background}
        return True

        
        
            
            








        
    