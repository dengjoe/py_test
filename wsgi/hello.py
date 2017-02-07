#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test wsgi module '

__author__ = 'Kevin deng'


# def application(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/html')])
#     return [b'<h1>Hello, web!</h1>']

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    print(method, path)
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]