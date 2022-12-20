FROM nvcr.io/nvidia/pytorch:22.09-py3

RUN apt update -y && apt install -y \
    python3-distutils \
    incron

WORKDIR /workspace
# install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

# setup incron
RUN echo "root" >> /etc/incron.allow
RUN echo "/workspace/2022-is-experiments2-team-3/src IN_CLOSE_WRITE,loopable=true cd /workspace/2022-is-experiments2-team-3 && make test" >> /var/spool/incron/root

COPY "./setup.sh" "/workspace/setup.sh"
RUN chmod 744 /workspace/setup.sh
CMD ["/workspace/setup.sh"]