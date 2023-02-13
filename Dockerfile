FROM fedora:latest
RUN dnf update -y
RUN dnf install -y python python-pip
RUN pip install cryptography
RUN pip install requests

ADD appA.py /home/appA.py
WORKDIR /home
CMD ["python", "./appA.py"]