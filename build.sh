#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

IMAGE=nvidia/cuda:12.1.0-devel-ubuntu18.04

docker pull ${IMAGE}

apt_command="apt update && apt install -y software-properties-common && add-apt-repository -y ppa:deadsnakes/ppa && apt update && apt install -y wget curl libtinfo-dev zlib1g-dev libssl-dev build-essential libedit-dev libxml2-dev"

install_python_env="curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3 && export PATH=~/miniconda3/bin/:$PATH && conda create -n py38 python=3.8 -y && conda create -n py39 python=3.9 -y && conda create -n py310 python=3.10 -y && conda create -n py311 python=3.11 -y && conda create -n py312 python=3.12 -y && ln -s ~/miniconda3/envs/py38/bin/python3.8 /usr/bin/python3.8 && ln -s ~/miniconda3/envs/py39/bin/python3.9 /usr/bin/python3.9 && ln -s ~/miniconda3/envs/py310/bin/python3.10 /usr/bin/python3.10 && ln -s ~/miniconda3/envs/py311/bin/python3.11 /usr/bin/python3.11 && ln -s ~/miniconda3/envs/py312/bin/python3.12 /usr/bin/python3.12 && conda install -y patchelf cmake"

install_pip="cd tilelang && python3.8 -m pip install  --upgrade pip && python3.8 -m pip install -r requirements-build.txt"

run_command="python3.8 -m tox -e py38,py39,py310,py311,py312,audit_2_27 && chown -R \${HOST_UID}:\${HOST_GID} /tilelang"

docker run --rm -v $(pwd):/tilelang \
  -e HOST_UID=$(id -u) \
  -e HOST_GID=$(id -g) \
  -e "http_proxy" \
  -e "https_proxy" \
  ${IMAGE} /bin/bash -c \
  "${apt_command} && \
  ${install_python_env} && \
  ${install_pip} && \
  ${run_command}"