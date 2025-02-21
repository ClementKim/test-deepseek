#!/bin/bash

ollama server &

ollama pull deepseek-r1:70b

python3 main.py 2> main-error

ollama rm deepseek-r1:70b

ollama stop

python3 test-under-8b.py 1.5 2> test-under-8b-error

rm -rf ~/.cache/huggingface
