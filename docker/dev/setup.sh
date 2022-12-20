echo "Setup Started"

# install pip packages
pip install build setuptools
pip install -e /workspace/2022-is-experiments2-team-3

echo "Setup Completed"

echo "SSH Server is runninng..."
# start ssh-server
/usr/sbin/sshd -D
