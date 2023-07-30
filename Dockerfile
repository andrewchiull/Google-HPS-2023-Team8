FROM francoisgervais/opencv-python


# set the working directory
WORKDIR /code

# VScode remote error
# node: error while loading shared libraries: libatomic.so.1
# [Sanity test failure for arm32v7/ubuntu · Issue #4675 · microsoft/vscode-remote-release](https://github.com/microsoft/vscode-remote-release/issues/4675)

RUN apt-get update ; apt-get install -y libatomic1

# install dependencies
# COPY ./requirements.txt ./
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# [python - Importing modules from parent folder - Stack Overflow](https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder)
COPY setup.py ./
RUN pip install --no-cache-dir -e .



# copy the src to the folder
COPY ./src ./src
COPY ./test_docker_volume.py .

CMD [ "python3", "-V" ]
