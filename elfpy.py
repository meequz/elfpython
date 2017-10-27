import sys


# FIXME
BANNED_WORDS = ['importlib._bootstr']


class Elframe:
    
    def __init__(self, frame):
        self.frame = frame
    
    def __str__(self):
        if not self.frame:
            return 'WTF?!'
        if self.is_module:
            return self.filename
        
        func_owner = self.class_type + self.class_id or self.filename
        if self.is_class:
            func_owner = '{}.{}'.format(self.filename, func_owner)
        output = '{}.{}()'.format(func_owner, self.func_name)
        return output
    
    @property
    def is_module(self):
        return self.frame and self.frame.f_code.co_name == '<module>'
    
    @property
    def is_class(self):
        return self.frame and 'self' in self.frame.f_locals
    
    @property
    def filename(self):
        if self.frame:
            return self.frame.f_code.co_filename[:-3]
    
    @property
    def func_name(self):
        if self.frame:
            return self.frame.f_code.co_name
    
    @property
    def class_id(self):
        if self.is_class:
            class_id_ = id(self.frame.f_locals['self'])
            return '({})'.format(class_id_)
        return ''
    
    @property
    def class_type(self):
        if self.is_class:
            return self.frame.f_locals['self'].__class__.__name__
        return ''


def check_banned_words(line):
    for word in BANNED_WORDS:
        if word in line:
            return True
    return False


def traceit(frame, event, arg):
    if event not in ['call', 'c_call']:
        return

    current_frame = Elframe(frame)
    parent_frame = Elframe(frame.f_back)
    line = '{} -> {}'.format(parent_frame, current_frame)
    if not check_banned_words(line):
        print(line)


sys.setprofile(traceit)