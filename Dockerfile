FROM dorakorpar/ubuntu:ns

WORKDIR /root/neural-style
RUN echo "alias nsgui='python gui.py'" >> /root/.bashrc
RUN apt-get install -y x11vnc xvfb
RUN apt-get install -y python-tk
RUN apt-get install -y eog

ADD gui.py /root/neural-style/
ENTRYPOINT ["/usr/bin/python"]
CMD ["gui.py"]