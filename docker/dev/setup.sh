echo "Setup Started"

# install pip packages
pip install -r /workspace/2022-is-experiments2-team-3/requirements.txt

echo "Setup Completed"

echo "SSH Server is runninng..."
# start ssh-server
/usr/sbin/sshd -D
