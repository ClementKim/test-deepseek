#!/bin/bash

start_time=$(date '+%s')

source test/bin/activate

full_start_time=$(date '+%s')

echo "running use-full-precision.py" >> log
python3 use-full-precision.py 1> result/full-stdout 2> result/full-stderr
echo "done for running use-full-precision.py" >> log

full_end_time=$(date '+%s')

full_diff=$((full_end_time - full_start_time))
full_hour=$((full_diff / 3600 % 24))
full_minute=$((full_diff / 60 % 60))
full_second=$((full_diff % 60))

echo "Total time: $full_hour h $full_minute m $full_second s" >> log

echo "removing ~/.cache/huggingface dir" >> log
rm -rf ~/.cache/huggingface
echo "done for removing" >> log

echo "ollama serve" >> log
ollama serve &

quantized_start_time=$(date '+%s')

echo "running use-quantized.py" >> log
python3 use-quantized.py 1> result/quantized-stdout 2> result/quantized-stderr
echo "done for running use-quantized.py" >> log

quantized_end_time=$(date '+%s')

quantized_diff=$((quantized_end_time - quantized_start_time))
quantized_hour=$((quantized_diff / 3600 % 24))
quantized_minute=$((quantized_diff / 60 % 60))
quantized_second=$((quantized_diff % 60))

echo "Total time: $quantized_hour h $quantized_minute m $quantized_second s" >> log

echo "removing deepseek r1 distill llama 70b" >> log
ollama rm deepseek-r1:70b

end_time=$(date '+%s')

diff=$((end_time - start_time))
hour=$((diff / 3600 % 24))
minute=$((diff / 60 % 60))
second=$((diff % 60))

echo "Total time: $hour h $minute m $second s" >> log

deactivate
