FROM nvcr.io/nvidia/pytorch:22.09-py3

RUN apt update -y && apt install -y \
    openssh-server \
    python3-distutils
RUN mkdir /var/run/sshd
RUN echo "root:isteam3" | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH Login時にPATHがデフォルトと違うものになる対策
RUN sed -i 's/#PermitUserEnvironment no/PermitUserEnvironment yes/' /etc/ssh/sshd_config
COPY "./environment" "/root/.ssh/environment"
RUN echo 'export PATH="$DEFAULT_PATH:$PATH"' >> /root/.bashrc

WORKDIR /workspace
# install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

EXPOSE 22
COPY "./setup.sh" "/workspace/setup.sh"
RUN chmod 744 /workspace/setup.sh
CMD ["/workspace/setup.sh"]