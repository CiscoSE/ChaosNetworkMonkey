#!/usr/bin/python
# -*- coding: utf-8 -*-


def resolveUser(name):
    if name is not None:
        if name.lower() == 'alice':
            return '10.10.22.114'
        elif name.lower() == 'bob':
            return '10.10.22.70'
    return 'error'


def main():
    print 'Main of resolveUser called'


if __name__ == '__main__':
    main()
