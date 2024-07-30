# Base image
FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-devel

# Set args
ARG DEBIAN_FRONTEND=noninteractive

# Set directory
WORKDIR /workspace

# Install base utilities
RUN apt-get update && \
    apt-get install -y apt-utils && \
    apt-get install -y build-essential wget git nano vim ffmpeg libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --upgrade pip

COPY tmp_build_requirements.txt /workspace/requirements.txt
RUN yes | pip install -r /workspace/requirements.txt

# Expose port
EXPOSE 4321

# Run command as entrypoint: jupyter notebook --no-browser --allow-root --ip=0.0.0.0 --port=4321 --NotebookApp.token='' --NotebookApp.password=''
ENTRYPOINT [ "jupyter", "notebook", "--no-browser", "--allow-root", "--ip=0.0.0.0", "--port=4321", "--NotebookApp.token=''", "--NotebookApp.password=''" ]
