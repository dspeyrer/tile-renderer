import pygame
import os
import json
import pickle

_image = {}


class __Storage__:
    def parse(self, filename):
        file = open('config/' + filename.replace(':', '/') +
                    self.ext, 'r' + self.encoding)
        return self.parsefile(file)

    def write(self, filename, data):
        file = open('config/' + filename.replace(':', '/') +
                    self.ext, 'w' + self.encoding)
        return self.writefile(file, data)

    def modify(self, filename, key, value):
        data = self.parse(filename)
        data[key] = value
        self.write(filename, data)

    def parsefile(self, file):
        raise NotImplementedError

    def writefile(self, file, data):
        raise NotImplementedError


''' STORES ANY OBJECT AS BINARY FILE '''


class __BinaryStorage__(__Storage__):
    ext = '.bin'
    encoding = 'b'

    def parsefile(self, file):
        return pickle.load(file)

    def writefile(self, file, data):
        return pickle.dump(data, file, pickle.DEFAULT_PROTOCOL)


''' STORES DICTIONARY OBJECT AS A TXT FILE '''


class __ConfStorage__(__Storage__):
    ext = '.txt'
    encoding = 't'

    def parsefile(self, file):
        ret = {}
        for line in file.readlines():
            i = line.split('=')
            ret[i[0]] = json.loads(i[1])
        return ret

    def writefile(self, file, data):
        ret = ''
        for i in data:
            ret += i + json.dumps(data[i]) + '\n'
        file.write(ret.strip())


STORAGE_BINARY = __BinaryStorage__()
STORAGE_CONF = __ConfStorage__()


def Img(path):
    global _image
    image = _image.get(path)
    if image == None:
        canonicalized_path = path.replace(
            '/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(
            'assets\\img\\' + canonicalized_path + '.png')
        _image[path] = image
    return image

def Dat(filename, method, *dat):
    if len(dat) == 0:
        return method.parse(filename)
    elif len(dat) == 1:
        return method.write(filename, dat[0])
    elif len(dat) == 2:
        return method.modify(filename, dat[0], dat[1])
