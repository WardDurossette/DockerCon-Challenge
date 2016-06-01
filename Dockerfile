FROM dorakorpar/ubuntu:ns

WORKDIR /root/neural-style
RUN echo "alias ngui='python gui.py'" >> /root/.bashrc
RUN apt-get install -y python-tk
ENV DISPLAY :0

ADD gui.py /root/neural-style/
ENTRYPOINT ["/usr/bin/python"]
CMD ["gui.py"]