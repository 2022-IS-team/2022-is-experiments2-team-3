echo "Setup Started"

# install pip packages
pip install -r /workspace/2022-is-experiments2-team-3/requirements.txt
pip install -e /workspace/2022-is-experiments2-team-3

echo "Setup Completed"

cd /workspace/2022-is-experiments2-team-3 && make run
