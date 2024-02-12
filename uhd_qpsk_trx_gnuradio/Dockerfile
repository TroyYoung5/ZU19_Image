FROM python:3.11-alpine
ENV PYTHONPATH "${PYTHONPATH}:/usr/lib/python3.11/site-packages:/usr/lib/python3.11/dist-packages:/usr/local/lib/python3.11/site-packages"
ENV LD_LIBRARY_PATH "${LD_LIBRARY_PATH}:/lib:/usr/lib:/usr/local/lib"
# set proxy variables
RUN export https_proxy=http://33717:Thu@10.20.28.20:8080 && \
    export HTTPS_PROXY=http://33717:Thu@10.20.28.20:8080 && \
    export HTTP_PROXY=http://33717:Thu@10.20.28.20:8080 && \
    export http_proxy=http://33717:Thu@10.20.28.20:8080 && \
    # add packages
    apk update && \
    apk add --no-cache gnuradio --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community \
    fmt=10.1.1-r0 --repository=https://dl-cdn.alpinelinux.org/alpine/edge/main \
    fmt-dev=10.1.1-r0 --repository=https://dl-cdn.alpinelinux.org/alpine/edge/main \
    #delete unecessary libs from python
    rm -rf /usr/lib/python3.11/site-packages/pyqtgraph && \
    rm -rf /usr/lib/python3.11/site-packages/PyQt5 && \
    rm -rf /usr/lib/python3.11/site-packages/qt5 && \
    rm -rf /usr/lib/python3.11/site-packages/OpenGL && \
    rm -rf /usr/lib/python3.11/site-packages/qt5 && \
    ldconfig /etc/ld.so.conf.d
