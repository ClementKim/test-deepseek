#!/bin/bash

source test/bin/activate

echo "ollama: pulling deepseek r1 distill llama 70b"
ollama pull deepseek-r1:70b

echo "running main.py"
python3 main.py 2> main-error

echo "removing deepseek r1 distill llama 70b"
ollama rm deepseek-r1:70b

echo "ollama stop"
ollama stop

deactivate
