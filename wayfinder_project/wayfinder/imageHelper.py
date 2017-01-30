import uuid
import os

def storeImageFunction(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('favourite_imgs', filename)