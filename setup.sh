
# Update and install system packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip git python3-venv nginx

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements (CPU-only torch)
pip install --upgrade pip
pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Run the FastAPI app in the background
nohup uvicorn app:app --host 127.0.0.1 --port 8000 &

